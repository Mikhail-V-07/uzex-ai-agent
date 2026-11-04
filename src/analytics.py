import duckdb


class Analytics:

    def __init__(self):
        self.con = duckdb.connect("data/uzex.duckdb")

    def total_deals(self):
        return self.con.execute("""
            SELECT COUNT(*)
            FROM deals
        """).fetchone()[0]

    def total_amount(self):
        return self.con.execute("""
            SELECT SUM(amount)
            FROM deals
        """).fetchone()[0]

    def deals_by_year(self):
        return self.con.execute("""
            SELECT
                YEAR("Дата сделки") AS year,
                COUNT(*) AS deals_count,
                SUM(amount) AS total_amount
            FROM deals
            GROUP BY year
            ORDER BY year
        """).fetchall()

    def top_products(self, limit=10):
        return self.con.execute("""
            SELECT
                "Наименование товара",
                COUNT(*) AS deals_count,
                SUM(amount) AS total_amount
            FROM deals
            GROUP BY "Наименование товара"
            ORDER BY total_amount DESC
            LIMIT ?
        """, [limit]).fetchall()

    def top_sellers(self, limit=10):
        return self.con.execute("""
            SELECT
                p."Наименование",
                COUNT(*) AS deals_count,
                SUM(d.amount) AS total_amount
            FROM deals d
            JOIN participants p
                ON d."ИНН продавца" = p."ИНН"
            GROUP BY p."ИНН", p."Наименование"
            ORDER BY total_amount DESC
            LIMIT ?
        """, [limit]).fetchall()

    def turnover_by_currency(self):
        return self.con.execute("""
            SELECT
                c."Валюта",
                COUNT(*) AS deals_count,
                SUM(d.amount) AS total_amount
            FROM deals d
            JOIN contracts c
                ON d."Номер контракта" = c."Номер контракта"
            GROUP BY c."Валюта"
            ORDER BY total_amount DESC
        """).fetchall()

    def deals_by_region(self):
        return self.con.execute("""
            SELECT
                "Регион",
                COUNT(*) AS deals_count,
                SUM(amount) AS total_amount
            FROM deals
            GROUP BY "Регион"
            ORDER BY deals_count DESC
        """).fetchall()

    def deals_by_status(self):
        return self.con.execute("""
            SELECT
                "Состояние сделки",
                COUNT(*) AS deals_count,
                SUM(amount) AS total_amount
            FROM deals
            GROUP BY "Состояние сделки"
            ORDER BY deals_count DESC
        """).fetchall()

    def deals_by_trade_type(self):
        return self.con.execute("""
            SELECT
                "Тип торгов",
                COUNT(*) AS deals_count,
                SUM(amount) AS total_amount
            FROM deals
            GROUP BY "Тип торгов"
            ORDER BY deals_count DESC
        """).fetchall()

    def top_buyers(self, limit=10):
        return self.con.execute("""
            SELECT
                p."Наименование",
                COUNT(*) AS deals_count,
                SUM(d.amount) AS total_amount
            FROM deals d
            JOIN participants p
                ON d."ИНН покупателя" = p."ИНН"
            GROUP BY p."ИНН", p."Наименование"
            ORDER BY total_amount DESC
            LIMIT ?
        """, [limit]).fetchall()

    def monthly_statistics(self, year):
        return self.con.execute("""
            SELECT
                MONTH("Дата сделки") AS month,
                COUNT(*) AS deals_count,
                SUM(amount) AS total_amount
            FROM deals
            WHERE YEAR("Дата сделки") = ?
            GROUP BY month
            ORDER BY month
        """, [year]).fetchall()

    def completed_deals(self):
        return self.con.execute("""
            SELECT
                COUNT(*) AS deals_count,
                SUM(amount) AS total_amount
            FROM deals
            WHERE "Состояние сделки" = 'Исполнен'
        """).fetchone()

    def close(self):
        self.con.close()


if __name__ == "__main__":
    analytics = Analytics()

    print("Всего сделок:", analytics.total_deals())
    print("Общая сумма сделок:", analytics.total_amount())

    print("\nСделки по годам:")
    for row in analytics.deals_by_year():
        print(row)

    print("\nТоп-10 товаров:")
    for row in analytics.top_products():
        print(row)

    print("\nТоп-10 продавцов:")
    for row in analytics.top_sellers():
        print(row)

    print("\nОборот по валютам:")
    for row in analytics.turnover_by_currency():
        print(row)

    print("\nТоп-10 покупателей:")
    for row in analytics.top_buyers():
        print(row)

    print("\nСтатистика по регионам:")
    for row in analytics.deals_by_region():
        print(row)

    print("\nСтатистика по состояниям:")
    for row in analytics.deals_by_status():
        print(row)

    print("\nСтатистика по типам торгов:")
    for row in analytics.deals_by_trade_type():
        print(row)

    print("\nИсполненные сделки:")
    print(analytics.completed_deals())

    print("\nСтатистика за 2025 год:")
    for row in analytics.monthly_statistics(2025):
        print(row)

    analytics.close()