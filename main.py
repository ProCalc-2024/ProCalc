import streamlit as st

from streamlit_gsheets import GSheetsConnection

# Create GSheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Demo Births DataFrame
df = psql.load_births()

# click button to update worksheet
# This is behind a button to avoid exceeding Google API Quota
if st.button("Create new worksheet"):
    df = conn.create(
        worksheet="Example 1",
        data=df,
    )
    st.cache_data.clear()
    st.rerun()

# Display our Spreadsheet as st.dataframe
st.dataframe(df.head(10))

