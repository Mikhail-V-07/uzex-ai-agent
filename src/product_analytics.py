
import duckdb


def main():
    con = duckdb.connect("data/uzex.duckdb")

    print("ТОП-15 ГРУПП ПО ОБОРОТУ В СУМАХ")

    rows = con.execute("""
        SELECT
            c."Код ТН ВЭД" AS tn_ved,
            COUNT(DISTINCT d."Номер сделки") AS deals_count,
            ROUND(SUM(d.amount_uzs), 2) AS turnover_uzs,
            COUNT(DISTINCT c."Наименование продукта") AS product_names
        FROM deals_financial d
        JOIN contracts c
            ON d."Номер контракта" = c."Номер контракта"
        WHERE c."Код ТН ВЭД" IS NOT NULL
          AND d.amount_uzs IS NOT NULL
        GROUP BY c."Код ТН ВЭД"
        ORDER BY turnover_uzs DESC
        LIMIT 15
    """).fetchall()

    for row in rows:
        print(row)

    print("\nТОП-15 КОНКРЕТНЫХ ТОВАРОВ ПО ОБОРОТУ")

    rows = con.execute("""
        SELECT
            c."Наименование продукта",
            c."Марка товара",
            c."Сорт товара",
            c."Класс товара",
            c."Единица измерения",
            COUNT(DISTINCT d."Номер сделки") AS deals_count,
            ROUND(SUM(d.amount_uzs), 2) AS turnover_uzs
        FROM deals_financial d
        JOIN contracts c
            ON d."Номер контракта" = c."Номер контракта"
        WHERE d.amount_uzs IS NOT NULL
        GROUP BY
            c."Наименование продукта",
            c."Марка товара",
            c."Сорт товара",
            c."Класс товара",
            c."Единица измерения"
        ORDER BY turnover_uzs DESC
        LIMIT 15
    """).fetchall()

    for row in rows:
        print(row)

    con.close()


if __name__ == "__main__":
    main()
