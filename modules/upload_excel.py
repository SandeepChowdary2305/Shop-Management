import streamlit as st
import pandas as pd
from utils.db_config import get_connection

def upload_products_from_excel():
    st.header("Upload Products from Excel")

    uploaded_file = st.file_uploader("Upload Excel (.xlsx) file for Products", type=["xlsx"], key="prod_upload")
    
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)

            required_columns = {"product_id", "name", "category", "cost_price", "stock"}
            if not required_columns.issubset(df.columns):
                st.error(f"Excel must contain columns: {', '.join(required_columns)}")
                return

            st.success("Product file uploaded successfully!")
            st.dataframe(df.head())

            if st.button("Insert Products into Database"):
                conn = get_connection()
                cursor = conn.cursor()

                for _, row in df.iterrows():
                    query = """
                        INSERT INTO products (product_id, name, category, cost_price, stock)
                        VALUES (%s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                          name = VALUES(name),
                          category = VALUES(category),
                          cost_price = VALUES(cost_price),
                          stock = VALUES(stock)
                    """
                    cursor.execute(query, (
                        row['product_id'], row['name'], row['category'], row['cost_price'], row['stock']
                    ))

                conn.commit()
                cursor.close()
                conn.close()

                st.success("Products inserted/updated successfully!")

        except Exception as e:
            st.error(f"Error reading product file: {e}")

def upload_sales_from_excel():
    st.header("Upload Sales from Excel")

    uploaded_file = st.file_uploader("Upload Excel (.xlsx) file for Sales", type=["xlsx"], key="sales_upload")
    
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)

            required_columns = {"sale_id", "product_id", "quantity", "selling_price", "sale_date"}
            if not required_columns.issubset(df.columns):
                st.error(f"Excel must contain columns: {', '.join(required_columns)}")
                return

            # Convert sale_date to datetime, with error check
            df['sale_date'] = pd.to_datetime(df['sale_date'], errors='coerce')
            if df['sale_date'].isnull().any():
                st.error("Some 'sale_date' values could not be parsed. Please fix the data.")
                return

            st.success("Sales file uploaded successfully!")
            st.dataframe(df.head())

            if st.button("Insert Sales into Database"):
                conn = get_connection()
                cursor = conn.cursor()

                for _, row in df.iterrows():
                    query = """
                        INSERT INTO sales (sale_id, product_id, quantity, selling_price, sale_date)
                        VALUES (%s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            product_id = VALUES(product_id),
                            quantity = VALUES(quantity),
                            selling_price = VALUES(selling_price),
                            sale_date = VALUES(sale_date)
                    """
                    cursor.execute(query, (
                        row['sale_id'], row['product_id'], row['quantity'],
                        row['selling_price'], row['sale_date']
                    ))

                conn.commit()
                cursor.close()
                conn.close()

                st.success("Sales inserted/updated successfully!")

        except Exception as e:
            st.error(f"Error reading sales file: {e}")

def main():
    st.title("Shop Management Uploads")

    st.caption("**Product Excel file headers must be:** `product_id`, `name`, `category`, `cost_price`, `stock`")
    st.caption("**Sales Excel file headers must be:** `sale_id`, `product_id`, `quantity`, `selling_price`, `sale_date`")

    upload_option = st.radio("Choose upload type", ("Upload Products", "Upload Sales"))

    if upload_option == "Upload Products":
        upload_products_from_excel()
    else:
        upload_sales_from_excel()


if __name__ == "__main__":
    main()
