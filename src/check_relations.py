import duckdb


def main():
    con = duckdb.connect("data/uzex.duckdb")

    checks = {
        "Сделки без найденного контракта": """
            SELECT COUNT(*)
            FROM deals d
            LEFT JOIN contracts c
                ON d."Номер контракта" = c."Номер контракта"
            WHERE c."Номер контракта" IS NULL
        """,

        "Сделки без найденного продавца": """
            SELECT COUNT(*)
            FROM deals d
            LEFT JOIN participants p
                ON d."ИНН продавца" = p."ИНН"
            WHERE d."ИНН продавца" IS NOT NULL
              AND p."ИНН" IS NULL
        """,

        "Сделки без найденного покупателя": """
            SELECT COUNT(*)
            FROM deals d
            LEFT JOIN participants p
                ON d."ИНН покупателя" = p."ИНН"
            WHERE d."ИНН покупателя" IS NOT NULL
              AND p."ИНН" IS NULL
        """,

        "Сделки без найденного брокера продавца": """
            SELECT COUNT(*)
            FROM deals d
            LEFT JOIN brokers b
                ON d."Брокер продавца" = CAST(b."Код брокера" AS VARCHAR)
            WHERE d."Брокер продавца" IS NOT NULL
              AND b."Код брокера" IS NULL
        """,

        "Сделки без найденного брокера покупателя": """
            SELECT COUNT(*)
            FROM deals d
            LEFT JOIN brokers b
                ON d."Брокер покупателя" = CAST(b."Код брокера" AS VARCHAR)
            WHERE d."Брокер покупателя" IS NOT NULL
              AND b."Код брокера" IS NULL
        """
    }

    for name, query in checks.items():
        result = con.execute(query).fetchone()[0]
        print(f"{name}: {result:,}")

    con.close()


if __name__ == "__main__":
    main()