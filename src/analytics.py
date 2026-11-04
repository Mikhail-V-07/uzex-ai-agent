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
        """Топ товаров по обороту в UZS."""

        return self.con.execute("""
            SELECT
                "Наименование товара",
                COUNT(*) AS deals_count,
                SUM(amount_uzs) AS turnover_uzs
            FROM deals_financial
            WHERE amount_uzs IS NOT NULL
            GROUP BY "Наименование товара"
            ORDER BY turnover_uzs DESC
            LIMIT ?
        """, [limit]).fetchall()


    def top_sellers(self, limit=10):
        """Топ продавцов по обороту в UZS."""

        return self.con.execute("""
            SELECT
                p."Наименование",
                COUNT(*) AS deals_count,
                SUM(d.amount_uzs) AS turnover_uzs
            FROM deals_financial d
            JOIN participants p
                ON d."ИНН продавца" = p."ИНН"
            WHERE d.amount_uzs IS NOT NULL
            GROUP BY p."ИНН", p."Наименование"
            ORDER BY turnover_uzs DESC
            LIMIT ?
        """, [limit]).fetchall()


    
    def total_turnover_uzs(self):
        """Общий оборот всех сделок в узбекских сумах."""

        result = self.con.execute("""
            SELECT
                SUM(
                    CASE
                        WHEN c."Валюта" = 'Доллар США'
                            THEN d.amount * r."Курс"
                        WHEN c."Валюта" = 'Узбекский сум'
                            THEN d.amount
                    END
                )
            FROM deals d
            JOIN contracts c
                ON d."Номер контракта" = c."Номер контракта"
            JOIN usd_rates r
                ON d."Дата сделки" = r."Дата"
            WHERE c."Валюта" IN ('Доллар США', 'Узбекский сум')
        """).fetchone()

        return result[0] or 0


    def turnover_by_year_uzs(self):
        """Оборот в UZS по годам."""

        return self.con.execute("""
            SELECT
                EXTRACT(YEAR FROM d."Дата сделки") AS year,
                COUNT(*) AS deals_count,
                SUM(
                    CASE
                        WHEN c."Валюта" = 'Доллар США'
                            THEN d.amount * r."Курс"
                        WHEN c."Валюта" = 'Узбекский сум'
                            THEN d.amount
                    END
                ) AS turnover_uzs
            FROM deals d
            JOIN contracts c
                ON d."Номер контракта" = c."Номер контракта"
            JOIN usd_rates r
                ON d."Дата сделки" = r."Дата"
            WHERE c."Валюта" IN ('Доллар США', 'Узбекский сум')
            GROUP BY year
            ORDER BY year
        """).fetchall()


    def turnover_by_currency(self):
        """Оборот отдельно по исходной валюте и в пересчёте на UZS."""

        return self.con.execute("""
            SELECT
                c."Валюта",
                COUNT(*) AS deals_count,
                SUM(d.amount) AS original_amount,
                SUM(
                    CASE
                        WHEN c."Валюта" = 'Доллар США'
                            THEN d.amount * r."Курс"
                        WHEN c."Валюта" = 'Узбекский сум'
                            THEN d.amount
                    END
                ) AS turnover_uzs
            FROM deals d
            JOIN contracts c
                ON d."Номер контракта" = c."Номер контракта"
            JOIN usd_rates r
                ON d."Дата сделки" = r."Дата"
            WHERE c."Валюта" IN ('Доллар США', 'Узбекский сум')
            GROUP BY c."Валюта"
            ORDER BY c."Валюта"
        """).fetchall()


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
        """Статистика по регионам в UZS."""

        return self.con.execute("""
            SELECT
                "Регион",
                COUNT(*) AS deals_count,
                SUM(amount_uzs) AS turnover_uzs
            FROM deals_financial
            WHERE amount_uzs IS NOT NULL
            GROUP BY "Регион"
            ORDER BY turnover_uzs DESC
        """).fetchall()


    def deals_by_status(self):
        """Статистика по состояниям сделок в UZS."""

        return self.con.execute("""
            SELECT
                "Состояние сделки",
                COUNT(*) AS deals_count,
                SUM(amount_uzs) AS turnover_uzs
            FROM deals_financial
            WHERE amount_uzs IS NOT NULL
            GROUP BY "Состояние сделки"
            ORDER BY turnover_uzs DESC
        """).fetchall()


    def deals_by_trade_type(self):
        """Статистика по типам торгов в UZS."""

        return self.con.execute("""
            SELECT
                "Тип торгов",
                COUNT(*) AS deals_count,
                SUM(amount_uzs) AS turnover_uzs
            FROM deals_financial
            WHERE amount_uzs IS NOT NULL
            GROUP BY "Тип торгов"
            ORDER BY turnover_uzs DESC
        """).fetchall()


    def top_buyers(self, limit=10):
        """Топ покупателей по обороту в UZS."""

        return self.con.execute("""
            SELECT
                p."Наименование",
                COUNT(*) AS deals_count,
                SUM(d.amount_uzs) AS turnover_uzs
            FROM deals_financial d
            JOIN participants p
                ON d."ИНН покупателя" = p."ИНН"
            WHERE d.amount_uzs IS NOT NULL
            GROUP BY p."ИНН", p."Наименование"
            ORDER BY turnover_uzs DESC
            LIMIT ?
        """, [limit]).fetchall()

    def monthly_statistics(self, year):
        """Статистика по месяцам в UZS."""

        return self.con.execute("""
            SELECT
                MONTH("Дата сделки") AS month,
                COUNT(*) AS deals_count,
                SUM(amount_uzs) AS turnover_uzs
            FROM deals_financial
            WHERE YEAR("Дата сделки") = ?
              AND amount_uzs IS NOT NULL
            GROUP BY month
            ORDER BY month
        """, [year]).fetchall()

    def completed_deals(self):
        """Количество и оборот исполненных сделок в UZS."""

        return self.con.execute("""
            SELECT
                COUNT(*) AS deals_count,
                SUM(amount_uzs) AS turnover_uzs
            FROM deals_financial
            WHERE "Состояние сделки" = 'Исполнен'
              AND amount_uzs IS NOT NULL
        """).fetchone()

    def top_normalized_products(self, limit=10):
        return self.con.execute("""
            SELECT
                c."Наименование продукта" AS product_name,
                c."Марка товара" AS brand,
                c."Сорт товара" AS product_sort,
                c."Класс товара" AS product_class,
                c."Код ТН ВЭД" AS tn_ved,
                c."Единица измерения" AS unit,
                COUNT(*) AS deals_count,
                SUM(d.amount_uzs) AS turnover_uzs
            FROM deals_financial d
            JOIN contracts c
                ON d."Номер контракта" = c."Номер контракта"
            GROUP BY
                c."Наименование продукта",
                c."Марка товара",
                c."Сорт товара",
                c."Класс товара",
                c."Код ТН ВЭД",
                c."Единица измерения"
            ORDER BY turnover_uzs DESC
            LIMIT ?
        """, [limit]).fetchall()

    def close(self):
        self.con.close()


if __name__ == "__main__":
    analytics = Analytics()

    
    print("\nОбщий оборот в UZS:")
    print(f"{analytics.total_turnover_uzs():,.2f}")

    print("\nОборот по годам в UZS:")
    for row in analytics.turnover_by_year_uzs():
        print(row)

    print("\nОборот по валютам:")
    for row in analytics.turnover_by_currency():
        print(row)


    print("Всего сделок:", analytics.total_deals())

    print("\nСделки по годам:")
    for row in analytics.turnover_by_year_uzs():
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

    print("\nТоп-10 нормализованных товаров:")
    for row in analytics.top_normalized_products(10):
        print(row)

    analytics.close()