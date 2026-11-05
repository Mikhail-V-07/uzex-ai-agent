"""Build an analytics-ready DuckDB database from the raw UZEX CSV export.

Raw CSVs (Russian headers, "1 234.5" numbers, DD.MM.YYYY dates) are converted into
clean, typed tables with English snake_case columns, plus one fully denormalised
`deals` table (deal + contract card + participants + brokers + USD rate + 100%
normalized product families, brands, sizes, sorts, types, classes, and regions)
so that the LLM can answer almost any question with a single-table query.

Also creates backwards-compatible views (`deals_financial`) for existing scripts.

Usage:  python src/build_db.py [path_to_csv_folder]
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

import duckdb
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from normalize import (  # noqa: E402
    REGIONS,
    brand_of,
    class_of,
    family_of,
    phonetic_key,
    size_of,
    sort_of,
    translit_key,
    type_of,
)

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA = Path(
    os.getenv(
        "UZEX_DATA_DIR",
        str(ROOT / "data" if (ROOT / "data" / "contracts.csv").exists() else ROOT.parent / "uzex_spot_data"),
    )
)
DB_PATH = Path(os.getenv("UZEX_DB_PATH", str(ROOT / "data" / "uzex.duckdb")))


def num(col: str) -> str:
    """'1 234 567.8' -> DOUBLE"""
    return f"TRY_CAST(REPLACE(REPLACE(\"{col}\", ' ', ''), chr(160), '') AS DOUBLE)"


def dt(col: str) -> str:
    return f"TRY_STRPTIME(\"{col}\", '%d.%m.%Y')::DATE"


def make_table(con: duckdb.DuckDBPyConnection, name: str, cols: list[str], rows: list) -> None:
    """Fast bulk load of Python rows."""
    df = pd.DataFrame([tuple(r) for r in rows], columns=cols).astype(object).where(lambda x: x.notna(), None)
    con.register("_df_tmp", df)
    con.execute(f"CREATE OR REPLACE TABLE {name} AS SELECT * FROM _df_tmp")
    con.unregister("_df_tmp")


def build(data_dir: Path | None = None, db_path: Path | None = None) -> None:
    data_dir = data_dir or DEFAULT_DATA
    db_path = db_path or DB_PATH
    t0 = time.time()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = db_path.with_suffix(".building")
    if tmp.exists():
        tmp.unlink()
    con = duckdb.connect(str(tmp))
    d = str(data_dir).replace("\\", "/")

    def raw(name: str, pattern: str) -> None:
        con.execute(
            f"CREATE TEMP TABLE {name} AS SELECT * FROM read_csv('{d}/{pattern}', header=true, "
            f"all_varchar=true, union_by_name=true, quote='\"', escape='\"')"
        )

    raw("raw_deals", "deals_*.csv")
    raw("raw_contracts", "contracts.csv")
    raw("raw_participants", "participants.csv")
    raw("raw_brokers", "brokers.csv")
    raw("raw_rates", "usd_rates.csv")

    # unify apostrophes in Uzbek region names (Farg`ona / Farg‘ona / Farg'ona ...)
    for t in ("raw_deals", "raw_participants", "raw_brokers"):
        con.execute(f"""UPDATE {t} SET "Регион" = regexp_replace("Регион", '[`''ʻ’ʼ]', '‘', 'g')""")

    # ---------------- reference tables ----------------
    make_table(con, "region_map", ["region", "region_ru", "region_contract_ru"], REGIONS)

    con.execute("""
        CREATE TABLE usd_rates AS
        SELECT TRY_STRPTIME("Дата", '%d.%m.%Y')::DATE AS rate_date,
               year(TRY_STRPTIME("Дата", '%d.%m.%Y')::DATE) AS year,
               month(TRY_STRPTIME("Дата", '%d.%m.%Y')::DATE) AS month,
               TRY_CAST("Курс" AS DOUBLE) AS usd_rate
        FROM raw_rates ORDER BY 1
    """)

    con.execute("""
        CREATE TABLE brokers AS
        SELECT b."Код брокера" AS broker_code,
               b."Наименование" AS broker_name,
               b."ИНН" AS broker_inn,
               b."Регион" AS region,
               rm.region_ru AS region_ru
        FROM raw_brokers b
        LEFT JOIN region_map rm ON rm.region = b."Регион"
        ORDER BY 1
    """)

    con.execute("""
        CREATE TABLE participants AS
        SELECT p."ИНН" AS inn,
               p."Наименование" AS name,
               p."Регион" AS region,
               rm.region_ru AS region_ru,
               p."Вид деятельности" AS activity,
               p."Роль" AS role,
               p."Плательщик НДС" AS vat_payer
        FROM raw_participants p
        LEFT JOIN region_map rm ON rm.region = p."Регион"
    """)

    # ---------------- contracts ----------------
    con.execute(f"""
        CREATE TABLE contracts_base AS
        SELECT TRY_CAST(c."Номер контракта" AS INTEGER) AS contract_id,
               c."Наименование продукта" AS product,
               c."Марка товара" AS brand,
               c."Размер товара" AS size,
               c."Сорт товара" AS sort,
               c."Тип товара" AS type,
               c."Класс товара" AS class,
               c."Код ТН ВЭД" AS hs_code,
               c."Группа товара" AS product_group,
               c."Категория товара" AS product_category,
               c."Отрасль промышленности" AS industry,
               c."Единица измерения" AS unit,
               TRY_CAST(c."Лот" AS INTEGER) AS lot_size,
               CASE c."Валюта" WHEN 'Доллар США' THEN 'USD' ELSE 'UZS' END AS currency,
               {num('Базисная цена')} AS base_price,
               TRY_CAST(REPLACE(REPLACE(c."Сумма залога", '%', ''), ' ', '') AS INTEGER) AS deposit_pct,
               c."Базис поставки" AS delivery_basis,
               c."Упаковка" AS packaging,
               rm.region AS region,
               rm.region_ru AS region_ru,
               c."Регион" AS region_contract_ru,
               c."Адрес склада" AS warehouse_address,
               c."Тип торгов" AS trade_type,
               c."Тип контракта" AS contract_type,
               c."Форма контракта" AS contract_form,
               TRY_CAST(c."Срок оплаты" AS INTEGER) AS payment_term_days,
               TRY_CAST(c."Срок поставки" AS INTEGER) AS delivery_term_days,
               c."ИНН продавца" AS seller_inn,
               sp.name AS seller_name,
               {dt('Дата регистрации')} AS registered_date,
               {dt('Действует до')} AS valid_until
        FROM raw_contracts c
        LEFT JOIN region_map rm ON rm.region_contract_ru = c."Регион"
        LEFT JOIN participants sp ON sp.inn = c."ИНН продавца"
    """)

    # Normalize all 6,616 contracts directly so even contracts without deals have full normalized fields
    contract_rows = con.execute("""
        SELECT DISTINCT contract_id, hs_code, product, brand, size, sort, type, class
        FROM contracts_base
    """).fetchall()
    cnorm = []
    for cid, hs, prod, brand, sz, srt, typ, cls in contract_rows:
        fam_ru, fam_uz = family_of(prod)
        cnorm.append((
            cid,
            fam_ru,
            fam_uz,
            brand_of(prod, brand, hs),
            size_of(prod, sz, hs),
            sort_of(prod, srt, hs),
            type_of(prod, typ, hs),
            class_of(prod, cls, hs),
        ))
    make_table(
        con,
        "tmp_cnorm",
        ["contract_id", "product_family", "product_family_uz", "brand_norm", "size_norm", "sort_norm", "type_norm", "class_norm"],
        cnorm,
    )

    con.execute("""
        CREATE TABLE contracts AS
        SELECT cb.*,
               cn.product_family,
               cn.product_family_uz,
               cn.brand_norm,
               cn.size_norm,
               cn.sort_norm,
               cn.type_norm,
               cn.class_norm
        FROM contracts_base cb
        LEFT JOIN tmp_cnorm cn ON cn.contract_id = cb.contract_id
        ORDER BY cb.contract_id
    """)
    con.execute("DROP TABLE contracts_base")
    con.execute("DROP TABLE tmp_cnorm")

    # ---------------- product_map for deal-level strings ----------------
    names = con.execute("""
        SELECT DISTINCT
               d."Наименование товара" AS product_name,
               c.product,
               c.hs_code,
               c.brand,
               c.size,
               c.sort,
               c.type,
               c.class
        FROM raw_deals d
        JOIN contracts c ON TRY_CAST(d."Номер контракта" AS INTEGER) = c.contract_id
    """).fetchall()
    pm_rows = []
    for deal_name, c_prod, hs, brand, sz, srt, typ, cls in names:
        fam_ru, fam_uz = family_of(c_prod or deal_name)
        combined = f"{c_prod or ''} {deal_name or ''}"
        pm_rows.append((
            deal_name,
            c_prod,
            fam_ru,
            fam_uz,
            brand_of(combined, brand, hs),
            size_of(combined, sz, hs),
            sort_of(combined, srt, hs),
            type_of(combined, typ, hs),
            class_of(combined, cls, hs),
        ))
    make_table(
        con,
        "product_map",
        ["product_name", "product", "product_family", "product_family_uz",
         "brand_norm", "size_norm", "sort_norm", "type_norm", "class_norm"],
        pm_rows,
    )

    # ---------------- deals (denormalised) ----------------
    con.execute(f"""
        CREATE TABLE deals AS
        WITH d AS (
            SELECT TRY_CAST("Номер сделки" AS BIGINT) AS deal_id,
                   {dt('Дата сделки')} AS deal_date,
                   TRY_CAST("Время сделки" AS TIME) AS deal_time,
                   "Тип торгов" AS trade_type,
                   TRY_CAST("Количество" AS BIGINT) AS quantity_lots,
                   {num('Сумма сделки')} AS amount,
                   {num('Стартовая цена')} AS start_price,
                   TRY_CAST("Номер контракта" AS INTEGER) AS contract_id,
                   "Наименование товара" AS product_name,
                   TRY_CAST("Лот" AS INTEGER) AS lot_size,
                   "Единица измерения" AS unit,
                   "Регион" AS region,
                   "Тип контракта" AS contract_type,
                   "Форма контракта" AS contract_form,
                   "Состояние сделки" AS status,
                   "ИНН продавца" AS seller_inn,
                   "ИНН покупателя" AS buyer_inn,
                   "Брокер продавца" AS seller_broker_code,
                   "Брокер покупателя" AS buyer_broker_code,
                   {dt('Дата оплаты')} AS payment_date,
                   {dt('Дата поставки')} AS delivery_date,
                   TRY_CAST("Поставлено" AS BIGINT) AS delivered_lots
            FROM raw_deals
        )
        SELECT d.deal_id,
               d.deal_date,
               d.deal_time,
               year(d.deal_date) AS year,
               month(d.deal_date) AS month,
               quarter(d.deal_date) AS quarter,
               d.trade_type,
               d.quantity_lots,
               d.lot_size,
               d.unit,
               CAST(d.quantity_lots * d.lot_size AS DOUBLE) AS volume,
               d.amount,
               c.currency,
               d.start_price,
               r.usd_rate,
               CASE WHEN c.currency = 'USD' THEN d.amount * r.usd_rate ELSE d.amount END AS amount_uzs,
               CASE WHEN c.currency = 'USD' THEN d.amount ELSE d.amount / r.usd_rate END AS amount_usd,
               CASE WHEN c.currency = 'USD' THEN d.start_price * r.usd_rate ELSE d.start_price END AS start_price_uzs,
               d.amount / NULLIF(d.quantity_lots * d.lot_size, 0) AS unit_price,
               (CASE WHEN c.currency = 'USD' THEN d.amount * r.usd_rate ELSE d.amount END) / NULLIF(d.quantity_lots * d.lot_size, 0) AS unit_price_uzs,
               (CASE WHEN c.currency = 'USD' THEN d.amount ELSE d.amount / r.usd_rate END) / NULLIF(d.quantity_lots * d.lot_size, 0) AS unit_price_usd,
               ((d.amount / NULLIF(d.quantity_lots * d.lot_size, 0)) - d.start_price) / NULLIF(d.start_price, 0) * 100.0 AS price_change_pct,
               d.contract_id,
               d.product_name,
               c.product,
               COALESCE(pm.product_family, c.product_family) AS product_family,
               COALESCE(pm.product_family_uz, c.product_family_uz) AS product_family_uz,
               c.brand,
               c.size,
               c.sort,
               c.type,
               c.class,
               COALESCE(pm.brand_norm, c.brand_norm) AS brand_norm,
               COALESCE(pm.size_norm, c.size_norm) AS size_norm,
               COALESCE(pm.sort_norm, c.sort_norm) AS sort_norm,
               COALESCE(pm.type_norm, c.type_norm) AS type_norm,
               COALESCE(pm.class_norm, c.class_norm) AS class_norm,
               c.hs_code,
               c.product_group,
               c.product_category,
               c.industry,
               d.region,
               rm.region_ru,
               c.warehouse_address,
               d.contract_type,
               d.contract_form,
               d.status,
               d.seller_inn,
               sp.name AS seller_name,
               sp.region AS seller_region,
               sp.region_ru AS seller_region_ru,
               sp.activity AS seller_activity,
               sp.vat_payer AS seller_vat_payer,
               d.buyer_inn,
               bp.name AS buyer_name,
               bp.region AS buyer_region,
               bp.region_ru AS buyer_region_ru,
               bp.activity AS buyer_activity,
               bp.vat_payer AS buyer_vat_payer,
               d.seller_broker_code,
               sb.broker_name AS seller_broker_name,
               sb.region AS seller_broker_region,
               d.buyer_broker_code,
               bb.broker_name AS buyer_broker_name,
               bb.region AS buyer_broker_region,
               d.payment_date,
               d.delivery_date,
               d.delivered_lots,
               CAST(d.delivered_lots * d.lot_size AS DOUBLE) AS delivered_volume,
               c.payment_term_days,
               c.delivery_term_days,
               (d.payment_date - d.deal_date) AS payment_days,
               (d.delivery_date - d.payment_date) AS delivery_days,
               CASE WHEN d.payment_date IS NOT NULL THEN (d.payment_date - d.deal_date) > c.payment_term_days ELSE NULL END AS is_late_payment,
               CASE WHEN d.delivery_date IS NOT NULL AND d.payment_date IS NOT NULL THEN (d.delivery_date - d.payment_date) > c.delivery_term_days ELSE NULL END AS is_late_delivery,
               c.base_price,
               c.deposit_pct,
               (CASE WHEN c.currency = 'USD' THEN d.amount * r.usd_rate ELSE d.amount END) * c.deposit_pct / 100.0 AS deposit_uzs,
               c.delivery_basis,
               c.packaging
        FROM d
        LEFT JOIN contracts c ON c.contract_id = d.contract_id
        LEFT JOIN product_map pm ON pm.product_name = d.product_name AND pm.product = c.product
        LEFT JOIN usd_rates r ON r.rate_date = d.deal_date
        LEFT JOIN region_map rm ON rm.region = d.region
        LEFT JOIN participants sp ON sp.inn = d.seller_inn
        LEFT JOIN participants bp ON bp.inn = d.buyer_inn
        LEFT JOIN brokers sb ON sb.broker_code = d.seller_broker_code
        LEFT JOIN brokers bb ON bb.broker_code = d.buyer_broker_code
        ORDER BY d.deal_id
    """)

    # ---------------- backwards-compatible view for legacy scripts ----------------
    con.execute("""
        CREATE OR REPLACE VIEW deals_financial AS
        SELECT
            deal_id AS "Номер сделки",
            deal_date AS "Дата сделки",
            deal_time AS "Время сделки",
            trade_type AS "Тип торгов",
            quantity_lots AS "Количество",
            CAST(amount AS VARCHAR) AS "Сумма сделки",
            CAST(start_price AS VARCHAR) AS "Стартовая цена",
            contract_id AS "Номер контракта",
            product_name AS "Наименование товара",
            lot_size AS "Лот",
            unit AS "Единица измерения",
            region AS "Регион",
            contract_type AS "Тип контракта",
            contract_form AS "Форма контракта",
            status AS "Состояние сделки",
            seller_inn AS "ИНН продавца",
            buyer_inn AS "ИНН покупателя",
            seller_broker_code AS "Брокер продавца",
            buyer_broker_code AS "Брокер покупателя",
            payment_date AS "Дата оплаты",
            delivery_date AS "Дата поставки",
            delivered_lots AS "Поставлено",
            amount,
            start_price,
            CASE currency WHEN 'USD' THEN 'Доллар США' ELSE 'Узбекский сум' END AS currency,
            amount_uzs
        FROM deals
    """)

    # ---------------- search index for fuzzy entity lookup ----------------
    ents = []
    for inn, name, role, region, region_ru, act in con.execute(
        "SELECT inn, name, role, region, region_ru, activity FROM participants"
    ).fetchall():
        ents.append(("company", inn, name, f"{role}; {region} ({region_ru}); {act}", translit_key(name), phonetic_key(name)))
    for code, name, region, region_ru in con.execute(
        "SELECT broker_code, broker_name, region, region_ru FROM brokers"
    ).fetchall():
        ents.append(("broker", code, name, f"{region} ({region_ru})", translit_key(name), phonetic_key(name)))
    for fam, fam_uz, hs_list, units, brands, n in con.execute("""
        SELECT product_family,
               any_value(product_family_uz),
               string_agg(DISTINCT hs_code, ','),
               string_agg(DISTINCT unit, '/'),
               string_agg(DISTINCT brand_norm, ', '),
               count(*)
        FROM deals GROUP BY 1
    """).fetchall():
        extra = f"uz={fam_uz}; hs_code={hs_list}; unit={units}; brands={brands or '-'}; deals={n}"
        t_str = f"{fam} {fam_uz or ''} {hs_list or ''}"
        ents.append(("product_family", fam, fam, extra, translit_key(t_str), phonetic_key(t_str)))
    for pname, fam, bnorm, snorm, cnorm, n in con.execute("""
        SELECT product_name,
               any_value(product_family),
               any_value(brand_norm),
               any_value(sort_norm),
               any_value(class_norm),
               count(*)
        FROM deals GROUP BY 1
    """).fetchall():
        extra = f"family={fam}; brand_norm={bnorm}; sort_norm={snorm}; class_norm={cnorm}; deals={n}"
        ents.append(("product_name", fam, pname, extra, translit_key(pname), phonetic_key(pname)))

    make_table(con, "entity_index", ["kind", "code", "name", "extra", "key", "pkey"], ents)

    # sanity checks
    n = con.execute(
        "SELECT count(*), count(contract_id), count(usd_rate), count(product_family), "
        "count(seller_name), count(buyer_name), count(seller_broker_name) FROM deals"
    ).fetchone()
    print("deals rows / joined:", n)
    con.close()
    if db_path.exists():
        db_path.unlink()
    tmp.rename(db_path)
    print(f"Built {db_path} in {time.time() - t0:.1f}s")


if __name__ == "__main__":
    data = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DATA
    build(data, DB_PATH)
