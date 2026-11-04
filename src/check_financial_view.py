
import duckdb


def main():
    con = duckdb.connect("data/uzex.duckdb")

    print("Количество сделок:")
    print(con.execute("""
        SELECT COUNT(*) FROM deals_financial
    """).fetchone()[0])

    print("\nОбщий оборот UZS:")
    print(con.execute("""
        SELECT SUM(amount_uzs)
        FROM deals_financial
    """).fetchone()[0])

    print("\nПроверка валют:")
    rows = con.execute("""
        SELECT
            currency,
            COUNT(*),
            SUM(amount_uzs)
        FROM deals_financial
        GROUP BY currency
    """).fetchall()

    for row in rows:
        print(row)

    con.close()


if __name__ == "__main__":
    main()
