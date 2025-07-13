import streamlit as st
from utils.db_config import get_connection



def add_product_ui():
    st.header("Add New Product")

    CATEGORIES = [
        "Electronics",
        "Grocery",
        "Clothing",
        "Stationery",
        "Toys",
        "Books",
        "Furniture",
        "Beauty",
    ]

    with st.form("add_product_form"):
        name = st.text_input("Product Name")
        category = st.selectbox("Category", CATEGORIES)
        cost_price = st.number_input("Cost Price", min_value=0.0, format="%.2f")
        # Removed selling_price input here
        stock = st.number_input("Stock Quantity", min_value=0, step=1)

        submitted = st.form_submit_button("Add Product")

        if submitted:
            if name and category and cost_price > 0 and stock >= 0:
                success = add_product(name, category, cost_price, stock)  # Updated call
                if success:
                    st.success(f"Product '{name}' added successfully!")
                else:
                    st.error("Failed to add product. Please try again.")
            else:
                st.error("Please fill all fields correctly.")

def add_product(name, category, cost_price, stock):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO products (name, category, cost_price, stock)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (name, category, cost_price, stock))  # Removed selling_price param
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            st.error(f"Database error: {e}")
            return False
    else:
        st.error("Database connection failed.")
        return False