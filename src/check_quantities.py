import duckdb


def main():
    con = duckdb.connect("data/uzex.duckdb")

    print("Проверка физических объёмов:")

    result = con.execute("""
        SELECT
            d."Единица измерения",
            COUNT(*) AS deals_count,
            SUM(
                TRY_CAST(d."Количество" AS DOUBLE) *
                TRY_CAST(d."Лот" AS DOUBLE)
            ) AS total_quantity
        FROM deals d
        GROUP BY d."Единица измерения"
        ORDER BY deals_count DESC
    """).fetchall()

    for row in result:
        print(row)

    print("\nПроверка сделок с нулевым или отсутствующим количеством:")

    invalid = con.execute("""
        SELECT COUNT(*)
        FROM deals
        WHERE TRY_CAST("Количество" AS DOUBLE) IS NULL
           OR TRY_CAST("Количество" AS DOUBLE) <= 0
           OR TRY_CAST("Лот" AS DOUBLE) IS NULL
           OR TRY_CAST("Лот" AS DOUBLE) <= 0
    """).fetchone()[0]

    print("Некорректных записей:", invalid)

    con.close()


if __name__ == "__main__":
    main()