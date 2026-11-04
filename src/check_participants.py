import duckdb


def main():
    con = duckdb.connect("data/uzex.duckdb")

    print("Всего участников:")
    print(con.execute("""
        SELECT COUNT(*)
        FROM participants
    """).fetchone()[0])

    print("\nУникальных ИНН:")
    print(con.execute("""
        SELECT COUNT(DISTINCT "ИНН")
        FROM participants
    """).fetchone()[0])

    print("\nПовторяющиеся ИНН:")
    print(con.execute("""
        SELECT
            "ИНН",
            COUNT(*) AS records
        FROM participants
        GROUP BY "ИНН"
        HAVING COUNT(*) > 1
        ORDER BY records DESC
        LIMIT 10
    """).fetchall())

    con.close()


if __name__ == "__main__":
    main()