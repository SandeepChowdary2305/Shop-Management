
import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='shopuser',
            password='Shop@123',
            database='shop_db'
        )
        return conn
    except Error as e:
        print("Database connection failed:", e)
        return None
