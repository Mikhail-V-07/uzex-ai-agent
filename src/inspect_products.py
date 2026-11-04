import duckdb

def main():
    con = duckdb.connect("data/uzex.duckdb")

    print("Примеры товаров и их характеристики:")

    rows = con.execute("""
        SELECT DISTINCT
            "Наименование продукта",
            "Марка товара",
            "Сорт товара",
            "Класс товара",
            "Код ТН ВЭД",
            "Группа товара",
            "Категория товара",
            "Единица измерения"
        FROM contracts
        LIMIT 30
    """).fetchall()

    for row in rows:
        print(row)

    con.close()


if __name__ == "__main__":
    main()