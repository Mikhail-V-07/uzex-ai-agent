import duckdb


def main():
    con = duckdb.connect("data/uzex.duckdb")

    print("Примеры сделок и размеров лотов:")

    result = con.execute("""
        SELECT
            d."Наименование товара",
            d."Количество",
            d."Лот",
            d."Единица измерения",
            c."Лот",
            c."Единица измерения"
        FROM deals d
        JOIN contracts c
            ON d."Номер контракта" = c."Номер контракта"
        LIMIT 15
    """).fetchall()

    for row in result:
        print(row)

    con.close()


if __name__ == "__main__":
    main()