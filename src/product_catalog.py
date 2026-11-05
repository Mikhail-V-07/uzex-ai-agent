import duckdb


def main():
    con = duckdb.connect("data/uzex.duckdb")

    con.execute("""
        CREATE OR REPLACE VIEW product_catalog AS
        SELECT
            "Код ТН ВЭД" AS tn_ved,
            "Наименование продукта" AS product_name,
            "Марка товара" AS brand,
            "Сорт товара" AS product_sort,
            "Класс товара" AS product_class,
            "Размер товара" AS product_size,
            "Тип товара" AS product_type,
            "Группа товара" AS product_group,
            "Категория товара" AS category,
            "Единица измерения" AS unit
        FROM contracts
    """)

    print("Количество товарных групп:")

    print(con.execute("""
        SELECT COUNT(DISTINCT tn_ved)
        FROM product_catalog
        WHERE tn_ved IS NOT NULL
    """).fetchone()[0])

    print("\nТоп-15 товарных групп по количеству контрактов:")

    rows = con.execute("""
        SELECT
            tn_ved,
            COUNT(*) AS contracts_count,
            COUNT(DISTINCT product_name) AS names_count,
            STRING_AGG(
                DISTINCT product_name,
                ' | '
            ) AS names
        FROM product_catalog
        WHERE tn_ved IS NOT NULL
        GROUP BY tn_ved
        ORDER BY contracts_count DESC
        LIMIT 15
    """).fetchall()

    for row in rows:
        print(row)

    con.close()


if __name__ == "__main__":
    main()