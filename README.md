# Business Sales Analytics System

## 1. Project Overview

The Business Sales Analytics System is a data analytics project developed using Python, Pandas, SQLite, SQL, and Microsoft Power BI.

The system analyzes sales transactions to understand business performance, product profitability, regional sales, and monthly revenue trends.

## 2. Objectives

- Analyze business sales data.
- Calculate revenue, total cost, profit, and profit margin.
- Identify top-performing products.
- Compare sales performance across regions.
- Analyze monthly sales trends.
- Store and query sales records using SQLite.
- Build an interactive Power BI dashboard.

## 3. Technologies Used

- **Python:** Main programming language.
- **Pandas:** Data processing and analysis.
- **SQLite:** Database storage.
- **SQL:** Data querying and aggregation.
- **Power BI Desktop:** Interactive data visualization.
- **CSV:** Data storage and report exchange.

## 4. Project Modules

### Module 1: Sales Data Analysis
Reads the CSV dataset, validates records, calculates revenue, cost, profit, and profit margin, and generates summary reports.

### Module 2: SQL Database
Loads the analyzed sales records into a SQLite database and verifies the stored data.

### Module 3: SQL Analytics
Uses SQL queries to analyze overall performance, product-wise sales, regional performance, monthly revenue, and top orders.

### Module 4: Power BI Dashboard
Displays key performance indicators, product revenue, monthly revenue trends, regional revenue, and interactive product and region filters.

## 5. Business Formulas

- Revenue = Quantity × Unit Price
- Total Cost = Quantity × Unit Cost
- Profit = Revenue − Total Cost
- Profit Margin (%) = (Total Profit ÷ Total Revenue) × 100

## 6. Dataset

The sample dataset contains 20 sales orders from January to April 2026.

Each record includes order ID, order date, product, category, region, quantity, unit cost, and unit price.

## 7. Sample Results

- Total orders: 20
- Total quantity sold: 123
- Total revenue: ₹683,850
- Total cost: ₹490,100
- Total profit: ₹193,750
- Profit margin: 28.33%

Laptop generated the highest revenue among the listed products. The North region generated the highest regional revenue, and March recorded the highest monthly revenue in the sample dataset.

## 8. How to Run

Install Pandas:

`python -m pip install pandas`

Run the sales analysis:

`python src/analyze_sales.py`

Load the analyzed data into SQLite:

`python src/load_to_sqlite.py`

Run SQL analytics:

`python src/sql_analysis.py`

Open `Business_Sales_Analytics.pbix` in Microsoft Power BI Desktop to view the dashboard.

Run the scripts from the project root directory.

## 9. Output Files

- `output/clean_sales_data.csv`
- `output/product_summary.csv`
- `output/region_summary.csv`
- `output/monthly_summary.csv`
- `database/sales.db`
- `Business_Sales_Analytics.pbix`

## 10. Limitations

The project currently uses a small sample dataset. It does not yet include live business data, automated scheduled refresh, user authentication, or a deployed web interface.

## 11. Future Enhancements

- Connect the system to live sales databases.
- Add automated data validation and testing.
- Build interactive sales forecasting.
- Add customer and inventory analysis.
- Publish dashboards and automate refresh where supported.
- Develop a web-based analytics interface.

## 12. Conclusion

The Business Sales Analytics System demonstrates an end-to-end analytics workflow using Python, Pandas, SQLite, SQL, and Power BI. It transforms raw sales records into structured data, business metrics, database queries, and an interactive dashboard.