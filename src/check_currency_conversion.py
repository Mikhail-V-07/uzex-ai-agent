
import duckdb


def main():
    con = duckdb.connect("data/uzex.duckdb")

    print("Результаты конвертации:")

    result = con.execute("""
        SELECT
            c."Валюта",
            COUNT(*) AS deals_count,
            COUNT(d.amount) AS valid_amounts,
            SUM(
                CASE
                    WHEN c."Валюта" = 'Доллар США'
                    THEN d.amount * r."Курс"
                    ELSE d.amount
                END
            ) AS total_uzs
        FROM deals d
        JOIN contracts c
            ON d."Номер контракта" = c."Номер контракта"
        JOIN usd_rates r
            ON CAST(d."Дата сделки" AS DATE) = r."Дата"
        GROUP BY c."Валюта"
    """).fetchall()

    for row in result:
        print(row)

    print("\nПримеры конвертации отдельных сделок:")

    rows = con.execute("""
        SELECT
            d."Номер сделки",
            d."Дата сделки",
            d.amount,
            c."Валюта",
            r."Курс",
            CASE
                WHEN c."Валюта" = 'Доллар США'
                THEN d.amount * r."Курс"
                ELSE d.amount
            END AS amount_uzs
        FROM deals d
        JOIN contracts c
            ON d."Номер контракта" = c."Номер контракта"
        JOIN usd_rates r
            ON CAST(d."Дата сделки" AS DATE) = r."Дата"
        WHERE c."Валюта" = 'Доллар США'
        LIMIT 5
    """).fetchall()

    for row in rows:
        print(row)

    con.close()


if __name__ == "__main__":
    main()
