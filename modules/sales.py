# modules/sales.py

import streamlit as st
from utils.db_config import get_connection

def record_sale_ui():
    st.header("Record a Sale")

    conn = get_connection()
    if not conn:
        st.error("Database connection failed.")
        return

    cursor = conn.cursor()
    cursor.execute("SELECT product_id, name, stock FROM products")
    products = cursor.fetchall()
    cursor.close()

    if not products:
        st.info("No products found. Please add products first.")
        return

    product_dict = {name: (pid, stock) for pid, name, stock in products}

    # Step 1: text input to filter products by partial name
    typed = st.text_input("Search product by name")

    # Step 2: filter product list
    if typed:
        filtered_products = [p for p in product_dict if typed.lower() in p.lower()]
    else:
        filtered_products = list(product_dict.keys())

    if not filtered_products:
        st.warning("No products match your search.")
        return

    # Step 3: selectbox with filtered results
    product_selected = st.selectbox("Select Product", filtered_products)

    pid, current_stock = product_dict[product_selected]

    quantity = st.number_input("Quantity Sold", min_value=1, step=1)
    selling_price = st.number_input("Selling Price per unit", min_value=0.0, format="%.2f")

    if st.button("Record Sale"):
        if quantity > current_stock:
            st.error(f"Not enough stock! Current stock: {current_stock}")
        else:
            if add_sale(pid, quantity, selling_price):
                update_stock(pid, current_stock - quantity)
                st.success(f"Sale recorded for {product_selected} (Qty: {quantity})")
            else:
                st.error("Failed to record sale. Try again.")

def add_sale(product_id, quantity, selling_price):
    conn = get_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO sales (product_id, quantity, selling_price)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (product_id, quantity, selling_price))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Database error: {e}")
        return False

def update_stock(product_id, new_stock):
    conn = get_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        query = "UPDATE products SET stock = %s WHERE product_id = %s"
        cursor.execute(query, (new_stock, product_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Database error: {e}")
        return False
