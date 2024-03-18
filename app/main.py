import pandas as pd
from database import Database
from utils import import_csv_to_dataframe, export_dataframe_to_csv

def query_sales_report(db):
    query = """
    SELECT
        p.category AS Category,
        c.region AS Region,
        TO_CHAR(o.order_date::DATE, 'Month') AS Month,
        SUM(o.quantity * o.unit_price) AS Total_Sales,
        SUM(o.quantity * (o.unit_price - p.purchase_price)) AS Margin
    FROM
        orders o
    JOIN
        products p ON o.product_id = p.product_id
    JOIN
        customers c ON o.customer_id = c.customer_id
    GROUP BY
        p.category,
        c.region,
        TO_CHAR(o.order_date::DATE, 'Month')
    ORDER BY
        p.category, c.region, Month;
    """
    return db.execute_query(query)

def query_customer_analysis(db):
    query = """
    WITH OrderDetails AS (
    SELECT 
        o.customer_id,
        o.order_date,
        LAG(o.order_date) OVER (PARTITION BY o.customer_id ORDER BY o.order_date) AS prev_order_date
    FROM 
        orders o
    )
    SELECT 
        c.customer_id as Customer_ID,
        c.region as Region,
        (
            SELECT 
                p.product_name
            FROM 
                orders o2
            JOIN 
                products p ON o2.product_id = p.product_id
            WHERE 
                o2.customer_id = c.customer_id
            GROUP BY 
                p.product_id, p.product_name
            ORDER BY 
                SUM(o2.quantity) DESC
            LIMIT 1
        ) AS Favorite_Category,
        COUNT(*) AS Total_Spent,
        SUM(o.quantity * o.unit_price) AS Favorite_Product,
        COALESCE(
            AVG(EXTRACT(EPOCH FROM (CAST(od.order_date AS TIMESTAMP) - CAST(od.prev_order_date AS TIMESTAMP)))) / (3600 * 24),
            0) AS Purchase_Frequency
    FROM 
        customers c
    JOIN 
        OrderDetails od ON c.customer_id = od.customer_id
    JOIN 
        orders o ON od.order_date = o.order_date
    GROUP BY 
        c.customer_id, c.region
    ORDER BY
        c.customer_id;
    """
    return db.execute_query(query) 

def main():
    db = Database(dbname='database', user='postgres', password='password', host='db')
    db.connect()

    customers_df = import_csv_to_dataframe('customers')
    products_df = import_csv_to_dataframe('products')
    orders_df = import_csv_to_dataframe('orders')


    if customers_df is not None:
        customers_df.to_sql("customers", db.engine, if_exists='replace', index=False)
    if products_df is not None:
        products_df.to_sql("products", db.engine, if_exists='replace', index=False)
    if orders_df is not None:
        orders_df.to_sql("orders", db.engine, if_exists='replace', index=False)

    sales_report_df = query_sales_report(db)
    customer_analysis_df = query_customer_analysis(db)

    export_dataframe_to_csv(sales_report_df, 'output/sales_report.csv')
    export_dataframe_to_csv(customer_analysis_df, 'output/customer_analysis.csv')

    db.close()

if __name__ == "__main__":
    main()
