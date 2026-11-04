
import duckdb
from pathlib import Path


class AnalyticsService:

    def __init__(self, db_path="data/uzex.duckdb"):
        self.db_path = Path(db_path)

        if not self.db_path.exists():
            raise FileNotFoundError(
                f"База данных не найдена: {self.db_path}"
            )

    def _query(self, sql):
        con = duckdb.connect(
            str(self.db_path),
            read_only=True
        )

        try:
            return con.execute(sql).fetchdf()
        finally:
            con.close()

    def get_summary(self):
        return self._query("""
            SELECT
                COUNT(*) AS deals_count,
                SUM(amount_uzs) AS turnover_uzs
            FROM deals_financial
        """)

    def get_yearly_turnover(self):
        return self._query("""
            SELECT
                YEAR("Дата сделки") AS year,
                COUNT(*) AS deals_count,
                SUM(amount_uzs) AS turnover_uzs
            FROM deals_financial
            GROUP BY YEAR("Дата сделки")
            ORDER BY year
        """)

    def get_top_products(self, limit=10):
        limit = max(1, min(int(limit), 50))

        return self._query(f"""
            SELECT
                c."Наименование продукта" AS product,
                c."Класс товара" AS product_class,
                c."Единица измерения" AS unit,
                COUNT(DISTINCT d."Номер сделки") AS deals_count,
                SUM(d.amount_uzs) AS turnover_uzs
            FROM deals_financial d
            JOIN contracts c
                ON d."Номер контракта" =
                   c."Номер контракта"
            WHERE d.amount_uzs IS NOT NULL
            GROUP BY
                c."Наименование продукта",
                c."Класс товара",
                c."Единица измерения"
            ORDER BY turnover_uzs DESC
            LIMIT {limit}
        """)

    def get_status_statistics(self):
        return self._query("""
            SELECT
                "Состояние сделки" AS status,
                COUNT(*) AS deals_count,
                SUM(amount_uzs) AS turnover_uzs
            FROM deals_financial
            GROUP BY "Состояние сделки"
            ORDER BY deals_count DESC
        """)
