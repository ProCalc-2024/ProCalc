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
    updated_orders = conn.copy()
    
    novo = ({
        'Materia': [materia] + updated_orders['Materia'],
        'Descrição': [descricao] + updated_orders['Descrição'],
        'Enunciado': [enunciado] + updated_orders['Enunciado'],
        'Alternativa_A': [letra_a] + updated_orders['Alternativa_A'],
        'Alternativa_B': [letra_b] + updated_orders['Alternativa_B'],
        'Alternativa_C': [letra_c] + updated_orders['Alternativa_C'],
        'Alternativa_D': [letra_d] + updated_orders['Alternativa_D'],
        'Alternativa_E': [letra_e] + updated_orders['Alternativa_E']
    })
    
    novo = pd.DataFrame(novo)
    
    if st.button("Salvar"):   

        if st.button("Update Worksheet"):
            conn.update(worksheet="Questõe", data=novo)
        st.success("Questão salva")
