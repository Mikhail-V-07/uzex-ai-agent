import duckdb

def main():
    con = duckdb.connect()

    query = """
    SELECT
        COUNT(*) AS total_rows,
        COUNT(*) FILTER (
            WHERE TRY_CAST(
                REGEXP_REPLACE("Сумма сделки", '[[:space:]]', '', 'g')
                AS DOUBLE
            ) IS NULL
        ) AS invalid_amounts,
        COUNT(*) FILTER (
            WHERE TRY_CAST(
                REGEXP_REPLACE("Стартовая цена", '[[:space:]]', '', 'g')
                AS DOUBLE
            ) IS NULL
        ) AS invalid_prices
    FROM read_csv(
        'data/deals_*.csv',
        header = true,
        union_by_name = true,
        encoding = 'utf-8'
    )
    """

    result = con.execute(query).fetchone()

    print(f"Всего сделок: {result[0]:,}")
    print(f"Некорректных сумм: {result[1]:,}")
    print(f"Некорректных стартовых цен: {result[2]:,}")

    con.close()


if __name__ == "__main__":
    main()