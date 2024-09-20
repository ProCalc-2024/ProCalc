import streamlit as st
import pandas as pd
import seaborn as sns
import gspread
from streamlit_gsheets import GSheetsConnection

# Create GSheets connection
st.title("Google Sheets as a DataBase")

# Function to create a sample Orders dataframe
def create_orders_dataframe():
    return pd.DataFrame({
        'OrderID': [101, 102, 103, 104, 105],
        'CustomerName': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'ProductList': ['ProductA, ProductB', 'ProductC', 'ProductA, ProductC', 'ProductB, ProductD', 'ProductD'],
        'TotalPrice': [200, 150, 250, 300, 100],
        'OrderDate': ['2023-08-18', '2023-08-19', '2023-08-19', '2023-08-20', '2023-08-20']
    })

# Create the Orders dataframe
orders = create_orders_dataframe()

# Update the TotalPrice column in the orders dataframe to create updated_orders
updated_orders = orders.copy()
updated_orders['TotalPrice'] = updated_orders['TotalPrice'] * 100

with st.expander("Data ⤵"):
    st.write("Orders")
    st.dataframe(orders)
    st.write("Updated Orders")
    st.dataframe(updated_orders)

st.divider()
st.write("CRUD Operations:")
# Establishing a Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

if st.button("Update Worksheet"):
    conn.update(worksheet="Questões", data=updated_orders)
    st.success("Worksheet Updated 🤓")

