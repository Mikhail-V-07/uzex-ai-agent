import duckdb
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_DB = ROOT / "data" / "uzex.duckdb"


class AnalyticsService:

    def __init__(self, db_path=None):
        self.db_path = Path(db_path) if db_path else DEFAULT_DB

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
                SUM(amount_uzs) AS turnover_uzs,
                SUM(amount_uzs) FILTER (WHERE status = 'Исполнен') AS executed_turnover_uzs,
                COUNT(*) FILTER (WHERE status = 'Исполнен') AS executed_deals_count,
                COUNT(DISTINCT seller_inn) AS sellers_count,
                COUNT(DISTINCT buyer_inn) AS buyers_count,
                COUNT(DISTINCT product_family) AS products_count
            FROM deals
        """)

    def get_yearly_turnover(self):
        return self._query("""
            SELECT
                year,
                COUNT(*) AS deals_count,
                SUM(amount_uzs) AS turnover_uzs,
                SUM(amount_uzs) FILTER (WHERE status = 'Исполнен') AS executed_turnover_uzs
            FROM deals
            GROUP BY year
            ORDER BY year
        """)

    def get_top_products(self, limit=15):
        limit = max(1, min(int(limit), 50))

        return self._query(f"""
            SELECT
                product_family AS product,
                product_family_uz AS product_uz,
                STRING_AGG(DISTINCT unit, ', ') AS unit,
                COUNT(*) AS deals_count,
                ROUND(SUM(amount_uzs), 2) AS turnover_uzs
            FROM deals
            WHERE amount_uzs IS NOT NULL
            GROUP BY product_family, product_family_uz
            ORDER BY turnover_uzs DESC
            LIMIT {limit}
        """)

    def get_status_statistics(self):
        return self._query("""
            SELECT
                status,
                COUNT(*) AS deals_count,
                ROUND(SUM(amount_uzs), 2) AS turnover_uzs
            FROM deals
            GROUP BY status
            ORDER BY deals_count DESC
        """)

    def get_region_statistics(self):
        return self._query("""
            SELECT
                region,
                region_ru,
                COUNT(*) AS deals_count,
                ROUND(SUM(amount_uzs), 2) AS turnover_uzs
            FROM deals
            GROUP BY region, region_ru
            ORDER BY turnover_uzs DESC
        """)
