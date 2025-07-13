# test_connection.py

from utils.db_config import get_connection

conn = get_connection()
if conn:
    print(" Connected to MySQL!")
    conn.close()
else:
    print(" Connection failed.")
