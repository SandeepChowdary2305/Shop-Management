import streamlit as st
from modules import product, sales, dashboard, forecast, upload_excel

# Initialize session state for menu tracking
if "menu" not in st.session_state:
    st.session_state.menu = "Add Product"  # default

# Sidebar Buttons
st.sidebar.title("Shop Management Menu")
if st.sidebar.button("Add Product"):
    st.session_state.menu = "Add Product"
if st.sidebar.button("Record Sale"):
    st.session_state.menu = "Record Sale"
if st.sidebar.button("Dashboard"):
    st.session_state.menu = "Dashboard"
if st.sidebar.button("Sales Forecast"):
    st.session_state.menu = "Sales Forecast"
if st.sidebar.button("Excel Upload"):
    st.session_state.menu = "Excel Upload"

# Menu Routing
choice = st.session_state.menu

if choice == "Add Product":
    product.add_product_ui()
elif choice == "Record Sale":
    sales.record_sale_ui()
elif choice == "Dashboard":
    dashboard.show_dashboard_ui()
elif choice == "Sales Forecast":
    forecast.forecast_sales_ui()
elif choice == "Excel Upload":
    st.subheader("Excel Upload Options")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Upload Products"):
            st.caption("**Product Excel file headers must be:** `product_id`, `name`, `category`, `cost_price`, `stock`")
            upload_excel.upload_products_from_excel()
    with col2:
        if st.button("Upload Sales"):
            st.caption("**Sales Excel file headers must be:** `sale_id`, `product_id`, `quantity`, `selling_price`, `sale_date`")
            upload_excel.upload_sales_from_excel()
