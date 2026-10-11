
from pathlib import Path
import sqlite3

# Find the database
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_FILE = PROJECT_ROOT / "database" / "sales.db"


def run_query(connection, title, query):
    print(f"\n========== {title} ==========")

    cursor = connection.cursor()
    cursor.execute(query)

    # Display column names
    columns = [description[0] for description in cursor.description]
    print(" | ".join(columns))
    print("-" * 65)

    # Display query results
    rows = cursor.fetchall()

    for row in rows:
        print(" | ".join(str(value) for value in row))


def main():
    if not DATABASE_FILE.exists():
        print("Database not found. Run load_to_sqlite.py first.")
        return

    with sqlite3.connect(DATABASE_FILE) as connection:

        # Query 1: Overall business performance
        run_query(
            connection,
            "OVERALL BUSINESS PERFORMANCE",
            """
            SELECT
                COUNT(DISTINCT OrderID) AS TotalOrders,
                SUM(Quantity) AS TotalQuantity,
                SUM(Revenue) AS TotalRevenue,
                SUM(TotalCost) AS TotalCost,
                SUM(Profit) AS TotalProfit,
                ROUND(
                    100.0 * SUM(Profit) / NULLIF(SUM(Revenue), 0),
                    2
                ) AS ProfitMarginPct
            FROM sales;
            """
        )

        # Query 2: Product-wise performance
        run_query(
            connection,
            "PRODUCT-WISE PERFORMANCE",
            """
            SELECT
                Product,
                SUM(Quantity) AS TotalQuantity,
                SUM(Revenue) AS TotalRevenue,
                SUM(Profit) AS TotalProfit
            FROM sales
            GROUP BY Product
            ORDER BY TotalRevenue DESC;
            """
        )

        # Query 3: Region-wise performance
        run_query(
            connection,
            "REGION-WISE PERFORMANCE",
            """
            SELECT
                Region,
                COUNT(DISTINCT OrderID) AS TotalOrders,
                SUM(Revenue) AS TotalRevenue,
                SUM(Profit) AS TotalProfit
            FROM sales
            GROUP BY Region
            ORDER BY TotalRevenue DESC;
            """
        )

        # Query 4: Monthly sales
        run_query(
            connection,
            "MONTHLY SALES",
            """
            SELECT
                SUBSTR(OrderDate, 1, 7) AS SalesMonth,
                SUM(Revenue) AS TotalRevenue,
                SUM(Profit) AS TotalProfit
            FROM sales
            GROUP BY SUBSTR(OrderDate, 1, 7)
            ORDER BY SalesMonth;
            """
        )

        # Query 5: Top three orders by revenue
        run_query(
            connection,
            "TOP THREE ORDERS BY REVENUE",
            """
            SELECT
                OrderID,
                Product,
                Quantity,
                Revenue,
                Profit
            FROM sales
            ORDER BY Revenue DESC
            LIMIT 3;
            """
        )

    print("\nSQL analysis completed successfully.")


if __name__ == "__main__":
    main()
