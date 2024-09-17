import streamlit as st
import pandas as pd
import seaborn as sns
from streamlit_gsheets import GSheetsConnection

# Create GSheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Demo Births DataFrame
df = sns.load_dataset('mpg')

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

