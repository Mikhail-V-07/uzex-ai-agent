import duckdb


def main():
    con = duckdb.connect("data/uzex.duckdb")

    queries = {
        "Валюты контрактов": """
            SELECT
                c."Валюта",
                COUNT(*) AS deals_count,
                SUM(d.amount) AS total_amount
            FROM deals d
            JOIN contracts c
                ON d."Номер контракта" = c."Номер контракта"
            GROUP BY c."Валюта"
            ORDER BY deals_count DESC
        """,

        "Состояния сделок": """
            SELECT
                "Состояние сделки",
                COUNT(*) AS deals_count
            FROM deals
            GROUP BY "Состояние сделки"
            ORDER BY deals_count DESC
        """,

        "Типы торгов": """
            SELECT
                "Тип торгов",
                COUNT(*) AS deals_count
            FROM deals
            GROUP BY "Тип торгов"
            ORDER BY deals_count DESC
        """,

        "Дубликаты номеров контрактов": """
            SELECT COUNT(*)
            FROM (
                SELECT "Номер контракта"
                FROM contracts
                GROUP BY "Номер контракта"
                HAVING COUNT(*) > 1
            )
        """,

        "Сделки без курса USD": """
            SELECT COUNT(*)
            FROM deals d
            LEFT JOIN usd_rates r
                ON d."Дата сделки" = r."Дата"
            WHERE r."Дата" IS NULL
        """
    }

    for title, query in queries.items():
        print(f"\n{'=' * 15} {title} {'=' * 15}")
        result = con.execute(query).fetchall()

        for row in result:
            print(row)

    con.close()


if __name__ == "__main__":
    main()