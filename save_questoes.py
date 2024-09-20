import streamlit as st
import pandas as pd
import gspread
from streamlit_gsheets import GSheetsConnection

# Create GSheets connection
st.title("Google Sheets as a DataBase")

def inserir_ques():    

    # adicionar uma nova pergunta
    result = {}

    col1, col2 = st.columns([1, 1])

    lista = [1,2,3]

    with col2:
        materia = st.selectbox("selecione uma materia", lista)

    with col1:
        descricao = st.text_input("descrição")

    enunciado = st.text_area("Enunciado", placeholder= "digite aqui o enunciado da questão")
    letra_a = st.text_input("Resposta1", placeholder= "digite aqui a resposta correta") 
    letra_b = st.text_input("Resposta2", placeholder= "digite aqui a resposta2")
    letra_c = st.text_input("Resposta3", placeholder= "digite aqui a resposta3") 
    letra_d = st.text_input("Resposta4", placeholder= "digite aqui a resposta4") 
    letra_e = st.text_input("Resposta5", placeholder= "digite aqui a resposta5")

    conn = st.connection("gsheets", type=GSheetsConnection)
    sheet = conn.read(worksheet="Questões")
    
    novo = ({
        'Materia': [materia] + sheet['Materia'],
        'Descrição': [descricao] + sheet['Descrição'],
        'Enunciado': [enunciado] + sheet['Enunciado'],
        'Alternativa_A': [letra_a] + sheet['Alternativa_A'],
        'Alternativa_B': [letra_b] + sheet['Alternativa_B'],
        'Alternativa_C': [letra_c] + sheet['Alternativa_C'],
        'Alternativa_D': [letra_d] + sheet['Alternativa_D'],
        'Alternativa_E': [letra_e] + sheet['Alternativa_E']
    })
    
    novo = pd.DataFrame(novo)
    
    if st.button("Salvar"):   

        conn.update(worksheet="Questões", data=novo)
        st.success("Questão salva")
    
    # New functionality to read the worksheet data
    if st.button("Read Worksheet"):
    # Fetch data from the Google Sheet
        sheet_data = conn.read(worksheet="Questões")
    
    # Check if data is returned
    if not sheet_data.empty:
        st.write("Data from Google Sheets:")
        st.dataframe(sheet_data)
    else:
        st.warning("No data found in the worksheet.")

# Executar a função principal
inserir_ques()
