import duckdb


def main():
    con = duckdb.connect("data/uzex.duckdb")

    print("Примеры курсов валют:")

    rows = con.execute("""
        SELECT "Дата", "Курс"
        FROM usd_rates
        ORDER BY "Дата"
        LIMIT 10
    """).fetchall()

    for row in rows:
        print(row)

    print("\nПоследние курсы:")

    rows = con.execute("""
        SELECT "Дата", "Курс"
        FROM usd_rates
        ORDER BY "Дата" DESC
        LIMIT 5
    """).fetchall()

    for row in rows:
        print(row)

    con.close()


if __name__ == "__main__":
    main()