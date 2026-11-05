import duckdb


def main():
    con = duckdb.connect("data/uzex.duckdb")

    print("Коды ТН ВЭД с несколькими названиями:")

    rows = con.execute("""
        SELECT
            "Код ТН ВЭД" AS tn_ved,
            COUNT(DISTINCT "Наименование продукта") AS names_count,
            STRING_AGG(
                DISTINCT "Наименование продукта",
                ' | '
            ) AS product_names
        FROM contracts
        WHERE "Код ТН ВЭД" IS NOT NULL
        GROUP BY "Код ТН ВЭД"
        HAVING COUNT(DISTINCT "Наименование продукта") > 1
        ORDER BY names_count DESC
        LIMIT 20
    """).fetchall()

    for row in rows:
        print(row)

    con.close()


if __name__ == "__main__":
    main()