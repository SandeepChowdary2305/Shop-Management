import mysql.connector
import random
from datetime import datetime, timedelta

# DB connection config
config = {
    'host': 'localhost',
    'user': 'shopuser',
    'password': 'Shop@123',
    'database': 'shop_db'
}

def random_date(start, end):
    """Generate random datetime between `start` and `end`"""
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)

    # Get all products with cost price
    cursor.execute("SELECT product_id, cost_price FROM products")
    products = cursor.fetchall()

    if not products:
        print("No products found in database.")
        exit()

    total_records = 10000
    start_date = datetime.now() - timedelta(days=730)  # 2 years ago
    end_date = datetime.now()

    print(f"🚀 Inserting {total_records} clean sales records...")

    for _ in range(total_records):
        product = random.choice(products)
        pid = product['product_id']
        cost = float(product['cost_price'])

        # Always selling above cost price (10% to 40% profit)
        selling_price = round(random.uniform(cost * 1.1, cost * 1.4), 2)
        quantity = random.randint(1, 5)
        sale_date = random_date(start_date, end_date).strftime('%Y-%m-%d %H:%M:%S')

        query = """
            INSERT INTO sales (product_id, quantity, selling_price, sale_date)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (pid, quantity, selling_price, sale_date))

    conn.commit()
    print("Successfully inserted 10,000+ clean sales records.")

except mysql.connector.Error as err:
    print(f"MySQL Error: {err}")

finally:
    cursor.close()
    conn.close()
