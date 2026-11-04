import duckdb


def main():
    con = duckdb.connect("data/uzex.duckdb")

    con.execute("""
        CREATE OR REPLACE VIEW normalized_products AS
        SELECT
            "Наименование продукта" AS product_name,
            "Марка товара" AS brand,
            "Сорт товара" AS product_sort,
            "Класс товара" AS product_class,
            "Код ТН ВЭД" AS tn_ved,
            "Группа товара" AS product_group,
            "Категория товара" AS category,
            "Единица измерения" AS unit,

            CONCAT(
                COALESCE(CAST("Код ТН ВЭД" AS VARCHAR), 'NO_CODE'),
                '|',
                COALESCE("Наименование продукта", ''),
                '|',
                COALESCE("Марка товара", ''),
                '|',
                COALESCE("Сорт товара", ''),
                '|',
                COALESCE("Класс товара", ''),
                '|',
                COALESCE("Единица измерения", '')
            ) AS product_key

        FROM contracts
    """)

    print("Всего записей в справочнике:")
    print(con.execute("""
        SELECT COUNT(*) FROM normalized_products
    """).fetchone()[0])

    print("\nУникальных товарных комбинаций:")
    print(con.execute("""
        SELECT COUNT(DISTINCT product_key)
        FROM normalized_products
    """).fetchone()[0])

    print("\nПримеры:")
    rows = con.execute("""
        SELECT DISTINCT
            product_name,
            brand,
            product_sort,
            product_class,
            tn_ved,
            unit,
            product_key
        FROM normalized_products
        LIMIT 10
    """).fetchall()

    for row in rows:
        print(row)

    con.close()


if __name__ == "__main__":
    main()