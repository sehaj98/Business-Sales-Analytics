
import unittest
import sqlite3
import pandas as pd
from pathlib import Path


class TestSalesAnalytics(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        project_root = Path(__file__).resolve().parents[1]
        csv_file = project_root / "data" / "sales_data.csv"

        cls.df = pd.read_csv(csv_file)

        cls.df["Revenue"] = (
            cls.df["Quantity"] * cls.df["UnitPrice"]
        )
        cls.df["TotalCost"] = (
            cls.df["Quantity"] * cls.df["UnitCost"]
        )
        cls.df["Profit"] = (
            cls.df["Revenue"] - cls.df["TotalCost"]
        )

    def test_dataset_has_20_orders(self):
        self.assertEqual(len(self.df), 20)

    def test_order_ids_are_unique(self):
        self.assertEqual(
            self.df["OrderID"].nunique(),
            len(self.df)
        )

    def test_total_quantity(self):
        self.assertEqual(self.df["Quantity"].sum(), 123)

    def test_total_revenue(self):
        self.assertEqual(self.df["Revenue"].sum(), 683850)

    def test_total_cost(self):
        self.assertEqual(self.df["TotalCost"].sum(), 490100)

    def test_total_profit(self):
        self.assertEqual(self.df["Profit"].sum(), 193750)

    def test_profit_formula(self):
        expected_profit = (
            self.df["Revenue"] - self.df["TotalCost"]
        )
        pd.testing.assert_series_equal(
            self.df["Profit"],
            expected_profit,
            check_names=False
        )

    def test_laptop_has_highest_revenue(self):
        revenue_by_product = (
            self.df.groupby("Product")["Revenue"].sum()
        )
        self.assertEqual(
            revenue_by_product.idxmax(),
            "Laptop"
        )

    def test_sqlite_stores_all_orders(self):
        # Use an in-memory database: no file-locking or cleanup issue.
        connection = sqlite3.connect(":memory:")

        try:
            self.df.to_sql(
                "sales",
                connection,
                if_exists="replace",
                index=False
            )

            count = connection.execute(
                "SELECT COUNT(*) FROM sales"
            ).fetchone()[0]

            total_revenue = connection.execute(
                "SELECT SUM(Revenue) FROM sales"
            ).fetchone()[0]

            self.assertEqual(count, 20)
            self.assertEqual(total_revenue, 683850)

        finally:
            connection.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
