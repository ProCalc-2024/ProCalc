import streamlit as st
import pandas as pd
import seaborn as sns
from streamlit_gsheets import GSheetsConnection

# Create GSheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Demo Meat DataFrame using seaborn sample data
df = sns.load_dataset('mpg')

# click button to update worksheet
# This is behind a button to avoid exceeding Google API Quota
if st.button("Update worksheet"):
    df = conn.update(
        worksheet="Questões",
        data=df,
    )
    # Clear cache after updating
    st.cache_data.clear()
    st.rerun()

# Display our Spreadsheet as st.dataframe
st.dataframe(df.head(10))

