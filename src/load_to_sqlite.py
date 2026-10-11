
from pathlib import Path
import sqlite3
import pandas as pd

# Project folders
PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV_FILE = PROJECT_ROOT / "output" / "clean_sales_data.csv"
DATABASE_DIR = PROJECT_ROOT / "database"
DATABASE_FILE = DATABASE_DIR / "sales.db"

def main():
    # Create database folder if needed
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)

    # Check that the Python analysis has generated its CSV
    if not CSV_FILE.exists():
        print("Error: clean_sales_data.csv not found.")
        print("Run analyze_sales.py first.")
        return

    # Read analyzed data
    df = pd.read_csv(CSV_FILE)

    # Connect to SQLite database
    with sqlite3.connect(DATABASE_FILE) as connection:
        # Store data in a SQL table named sales
        df.to_sql(
            "sales",
            connection,
            if_exists="replace",
            index=False
        )

        # Verify that the records were saved
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM sales")
        record_count = cursor.fetchone()[0]

        # Display a small sample
        cursor.execute("""
            SELECT OrderID, Product, Quantity, Revenue, Profit
            FROM sales
            ORDER BY OrderID
            LIMIT 5
        """)
        sample_records = cursor.fetchall()

    print("\n========== SQL DATABASE CREATED ==========")
    print(f"Database: {DATABASE_FILE}")
    print(f"Records stored: {record_count}")

    print("\nFirst five records:")
    for record in sample_records:
        print(record)

    print("\nData successfully loaded into the sales table.")

if __name__ == "__main__":
    main()
