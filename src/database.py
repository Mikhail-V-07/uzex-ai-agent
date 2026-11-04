import duckdb


def create_database():
    con = duckdb.connect("data/uzex.duckdb")

    # Сделки
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

    # Контракты
    con.execute("""
        CREATE OR REPLACE VIEW contracts AS
        SELECT *
        FROM read_csv(
            'data/contracts.csv',
            header = true,
            encoding = 'utf-8'
        )
    """)

    # Участники
    con.execute("""
        CREATE OR REPLACE VIEW participants AS
        SELECT *
        FROM read_csv(
            'data/participants.csv',
            header = true,
            encoding = 'utf-8'
        )
    """)

    # Брокеры
    con.execute("""
        CREATE OR REPLACE VIEW brokers AS
        SELECT *
        FROM read_csv(
            'data/brokers.csv',
            header = true,
            encoding = 'utf-8'
        )
    """)

    # Курсы валют
    con.execute("""
        CREATE OR REPLACE VIEW usd_rates AS
        SELECT *
        FROM read_csv(
            'data/usd_rates.csv',
            header = true,
            encoding = 'utf-8'
        )
    """)

    print("Проверка таблиц:")

    for table in ["deals", "contracts", "participants", "brokers", "usd_rates"]:
        count = con.execute(
            f"SELECT COUNT(*) FROM {table}"
        ).fetchone()[0]

        print(f"{table}: {count:,} строк")

    con.close()
    print("\\nВсе представления успешно созданы!")


if __name__ == "__main__":
    create_database()