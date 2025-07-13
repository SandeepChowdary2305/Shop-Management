import streamlit as st
import pandas as pd
from utils.db_config import get_connection
import matplotlib.pyplot as plt

def show_dashboard_ui():
    st.title("Shop Sales Overview")

    conn = get_connection()
    if not conn:
        st.error("Unable to connect to the database.")
        return

    query = """
        SELECT p.category, s.sale_date, s.quantity, s.selling_price, p.cost_price
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
    """

    df = pd.read_sql(query, conn)
    conn.close()

    if df.empty:
        st.info("No sales data found. Please record some sales first.")
        return

    # Convert sale_date to datetime
    df['sale_date'] = pd.to_datetime(df['sale_date'])

    # Calculate profit per sale
    df['profit'] = (df['selling_price'] - df['cost_price']) * df['quantity']

    st.sidebar.header("Filter Data by Date")
    min_date = df['sale_date'].min().date()
    max_date = df['sale_date'].max().date()

    start_date = st.sidebar.date_input("Start date", min_date, min_value=min_date, max_value=max_date)
    end_date = st.sidebar.date_input("End date", max_date, min_value=min_date, max_value=max_date)

    if start_date > end_date:
        st.sidebar.error("Start date must be before end date.")
        return

    # Filter dataframe
    mask = (df['sale_date'].dt.date >= start_date) & (df['sale_date'].dt.date <= end_date)
    filtered_df = df.loc[mask]

    if filtered_df.empty:
        st.warning("No sales data available for the selected date range.")
        return

    # Display key metrics
    total_sales_qty = filtered_df['quantity'].sum()
    total_profit = filtered_df['profit'].sum()
    total_revenue = (filtered_df['selling_price'] * filtered_df['quantity']).sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Items Sold", f"{total_sales_qty}")
    col2.metric("Total Revenue", f"₹{total_revenue:,.2f}")
    col3.metric("Total Profit", f"₹{total_profit:,.2f}")

    st.markdown("---")

    # Sales by category (Quantity)
    sales_by_cat = filtered_df.groupby('category')['quantity'].sum().sort_values(ascending=False)
    st.subheader("Items Sold by Category")
    st.bar_chart(sales_by_cat)

    # Profit by category
    profit_by_cat = filtered_df.groupby('category')['profit'].sum().sort_values(ascending=False)
    st.subheader("Profit by Category")
    st.bar_chart(profit_by_cat)

    # Daily sales trend (quantity)
    daily_sales = filtered_df.groupby(filtered_df['sale_date'].dt.date)['quantity'].sum()
    st.subheader("Daily Sales Trend")
    st.line_chart(daily_sales)

    # Daily profit trend
    daily_profit = filtered_df.groupby(filtered_df['sale_date'].dt.date)['profit'].sum()
    st.subheader("Daily Profit Trend")
    st.line_chart(daily_profit)

