import duckdb


def create_database():
    con = duckdb.connect("data/uzex.duckdb")

    con.execute("""
        CREATE OR REPLACE VIEW deals AS
        SELECT
            *,
            TRY_CAST(
                REGEXP_REPLACE("Сумма сделки", '[[:space:]]', '', 'g')
                AS DOUBLE
            ) AS amount,
            TRY_CAST(
                REGEXP_REPLACE("Стартовая цена", '[[:space:]]', '', 'g')
                AS DOUBLE
            ) AS start_price
        FROM read_csv(
            'data/deals_*.csv',
            header = true,
            union_by_name = true,
            encoding = 'utf-8'
        )
    """)

    con.close()
    print("База данных создана!")


if __name__ == "__main__":
    create_database()