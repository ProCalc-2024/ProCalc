import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("Read Google Sheet as DataFrame")

conn = st.connection("Bd_ProCalc", type=GSheetsConnection)
df = conn.read(worksheet="Questões")

st.dataframe(df)
