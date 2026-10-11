
from pathlib import Path
import pandas as pd

# 1. Set project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = PROJECT_ROOT / "data" / "sales_data.csv"
OUTPUT_DIR = PROJECT_ROOT / "output"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    # 2. Check whether the dataset exists
    if not DATA_FILE.exists():
        print(f"Error: Dataset not found at {DATA_FILE}")
        print("Please check that sales_data.csv is inside the data folder.")
        return

    # 3. Read CSV data using Pandas
    df = pd.read_csv(DATA_FILE)

    required_columns = [
        "OrderID", "OrderDate", "Product", "Category",
        "Region", "Quantity", "UnitCost", "UnitPrice"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        print("Error: Missing columns:", missing_columns)
        return

    # 4. Clean and validate data
    df["OrderDate"] = pd.to_datetime(
        df["OrderDate"], errors="coerce"
    )

    numeric_columns = [
        "OrderID", "Quantity", "UnitCost", "UnitPrice"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column], errors="coerce"
        )

    df = df.dropna(subset=required_columns)
    df = df.drop_duplicates(subset=["OrderID"])

    # Remove invalid sales records
    df = df[
        (df["Quantity"] > 0)
        & (df["UnitCost"] >= 0)
        & (df["UnitPrice"] >= 0)
    ].copy()

    if df.empty:
        print("Error: No valid sales records found.")
        return

    # 5. Calculate revenue, cost and profit
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]
    df["TotalCost"] = df["Quantity"] * df["UnitCost"]
    df["Profit"] = df["Revenue"] - df["TotalCost"]

    df["ProfitMarginPct"] = (
        df["Profit"] / df["Revenue"].replace(0, float("nan")) * 100
    ).round(2)

    # 6. Product-wise sales summary
    product_summary = (
        df.groupby("Product", as_index=False)
        .agg(
            TotalQuantity=("Quantity", "sum"),
            TotalRevenue=("Revenue", "sum"),
            TotalCost=("TotalCost", "sum"),
            TotalProfit=("Profit", "sum")
        )
        .sort_values("TotalRevenue", ascending=False)
    )

    # 7. Region-wise sales summary
    region_summary = (
        df.groupby("Region", as_index=False)
        .agg(
            TotalOrders=("OrderID", "nunique"),
            TotalRevenue=("Revenue", "sum"),
            TotalProfit=("Profit", "sum")
        )
        .sort_values("TotalRevenue", ascending=False)
    )

    # 8. Monthly sales summary
    df["Month"] = df["OrderDate"].dt.to_period("M").astype(str)

    monthly_summary = (
        df.groupby("Month", as_index=False)
        .agg(
            TotalOrders=("OrderID", "nunique"),
            TotalQuantity=("Quantity", "sum"),
            TotalRevenue=("Revenue", "sum"),
            TotalCost=("TotalCost", "sum"),
            TotalProfit=("Profit", "sum")
        )
        .sort_values("Month")
    )

    # 9. Calculate overall business performance
    total_revenue = df["Revenue"].sum()
    total_cost = df["TotalCost"].sum()
    total_profit = df["Profit"].sum()

    overall_margin = (
        total_profit / total_revenue * 100
        if total_revenue != 0 else 0
    )

    # 10. Display results in the terminal
    print("\n========== BUSINESS SALES ANALYTICS ==========")
    print(f"Valid orders       : {df['OrderID'].nunique()}")
    print(f"Total quantity sold: {df['Quantity'].sum():,.0f}")
    print(f"Total revenue      : Rs. {total_revenue:,.2f}")
    print(f"Total cost         : Rs. {total_cost:,.2f}")
    print(f"Total profit       : Rs. {total_profit:,.2f}")
    print(f"Profit margin      : {overall_margin:.2f}%")

    print("\n========== PRODUCT-WISE SUMMARY ==========")
    print(product_summary.to_string(index=False))

    print("\n========== REGION-WISE SUMMARY ==========")
    print(region_summary.to_string(index=False))

    print("\n========== MONTHLY SALES SUMMARY ==========")
    print(monthly_summary.to_string(index=False))

    # 11. Export reports for SQL and Power BI work
    df.to_csv(OUTPUT_DIR / "clean_sales_data.csv", index=False)
    product_summary.to_csv(
        OUTPUT_DIR / "product_summary.csv", index=False
    )
    region_summary.to_csv(
        OUTPUT_DIR / "region_summary.csv", index=False
    )
    monthly_summary.to_csv(
        OUTPUT_DIR / "monthly_summary.csv", index=False
    )

    print("\nReports saved successfully in the output folder.")
    print("Generated files:")
    print("- clean_sales_data.csv")
    print("- product_summary.csv")
    print("- region_summary.csv")
    print("- monthly_summary.csv")


if __name__ == "__main__":
    main()
