# 🛒 Shop Management System

A simple and interactive **Shop Management Dashboard** built using **Python**, **Streamlit**, and **MySQL**.  
This tool helps shopkeepers or small retailers manage products, record daily sales, and analyze profits easily through a clean and responsive UI.

---

## 🚀 Features

- 📦 **Add products** with name, category, cost price, and selling price  
- 🛒 **Record sales** with automatic date stamping  
- 📊 **View profit/loss analysis** (Daily, Weekly, Monthly, Yearly)  
- 📁 **Upload product data in bulk** from Excel (.xlsx) files  
- 🔮 **Forecast sales trends** using an LSTM-based model  

---

## 🧰 Tech Stack

| Layer       | Tools/Libraries                  |
| ----------- | -------------------------------|
| **UI**      | Streamlit                      |
| **Backend** | Python                        |
| **Database**| MySQL                        |
| **Data**    | Pandas, openpyxl               |
| **Forecast**| TensorFlow, Keras (LSTM Model) |

---

## 📁 Project Structure

```plaintext
shop_management/
├── app.py                   -> Main entry (Streamlit app)
├── test_connection.py       -> MySQL DB test script
├── insert_sample_sales.py   -> Script to insert dummy sales data

├── modules/                 -> Functional modules
│   ├── product.py           -> Add product logic & UI
│   ├── sales.py             -> Sales recording logic & UI
│   ├── dashboard.py         -> Profit analysis UI
│   ├── forecast.py          -> LSTM-based sales forecasting
│   └── upload_excel.py      -> Excel upload logic

├── utils/
│   └── db_config.py         -> MySQL DB configuration
```
---

## ⚙️ Setup Instructions
1. Prerequisites

- Python 3.10+
- MySQL server running locally or remotely

-Required packages:
```plaintext
pip install streamlit pandas mysql-connector-python openpyxl tensorflow
```

2. MySQL Database Setup
- Create a MySQL database named shop_db
- In ``` utils/db_config.py```, update your MySQL credentials:

```plaintext
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="your_mysql_user",
        password="your_password",
        database="shop_db"
    )
```
- You can use ```test_connection.py``` to verify the database connection.
---
## ▶️ Running the App
```plaintext
cd shop_management
streamlit run app.py
```
From the sidebar, you can:

- ➕ Add Products
- 🛒 Record Sales
- 📊 View Dashboard
- 📈 Forecast Sales
- 📥 Upload Products via Excel
---
## 📌 Notes
- All sales are timestamped with the current date.
- The dashboard gives dynamic, period-based summaries.
- Forecasting uses a basic LSTM model (can be expanded).
- Best suited for small-to-medium shopkeepers.
---
## 📄 License
This project is licensed under the MIT License.

You are free to use, modify, and distribute this software for personal, academic, or commercial purposes.
Check the LICENSE file for full license details.
---
## 👨‍💻 Author
Made with ❤️ by L Sandeep
