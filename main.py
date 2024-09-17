import streamlit as st
import pandas as pd
import seaborn as sns
from streamlit_gsheets import GSheetsConnection

# Create GSheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Demo Births DataFrame
df = pd.DataFrame({
        'OrderID': [101, 102, 103, 104, 105],
        'CustomerName': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'ProductList': ['ProductA, ProductB', 'ProductC', 'ProductA, ProductC', 'ProductB, ProductD', 'ProductD'],
        'TotalPrice': [200, 150, 250, 300, 100],
        'OrderDate': ['2023-08-18', '2023-08-19', '2023-08-19', '2023-08-20', '2023-08-20']
    })

# click button to update worksheet
# This is behind a button to avoid exceeding Google API Quota
if st.button("Create new worksheet"):
    df = conn.create(
        worksheet="Questões",
        data=df,
    )
    st.cache_data.clear()
    st.rerun()

# Display our Spreadsheet as st.dataframe
st.dataframe(df.head(10))

