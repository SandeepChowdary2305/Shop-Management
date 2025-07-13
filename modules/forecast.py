import streamlit as st
import pandas as pd
from prophet import Prophet
from utils.db_config import get_connection

def forecast_sales_ui():
    st.header("Sales Forecasting")

    conn = get_connection()
    if not conn:
        st.error("Database connection failed.")
        return

    query = """
    SELECT DATE(s.sale_date) as ds, p.category, SUM(s.quantity) as y
    FROM sales s
    JOIN products p ON s.product_id = p.product_id
    GROUP BY ds, p.category
    ORDER BY ds
    """

    df = pd.read_sql(query, conn)
    conn.close()

    if df.empty:
        st.info("No sales data available for forecasting.")
        return

    categories = df['category'].unique()
    selected_category = st.selectbox("Select Category to Forecast", categories)

    df_cat = df[df['category'] == selected_category][['ds', 'y']]
    df_cat['ds'] = pd.to_datetime(df_cat['ds'])

    if len(df_cat) < 2:
        st.warning(f"Not enough data points to forecast for category '{selected_category}'. Please select a different category or add more data.")
        return

    st.subheader("Historical Sales Data")
    st.line_chart(df_cat.set_index('ds')['y'])

    periods = st.number_input("Days to forecast", min_value=1, max_value=365, value=30)

    model = Prophet()
    model.fit(df_cat)

    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)

    st.subheader(f"Sales Forecast for next {periods} days - {selected_category}")
    fig = model.plot(forecast)
    st.pyplot(fig)
