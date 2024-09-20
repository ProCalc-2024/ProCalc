import streamlit as st
import pandas as pd
import gspread
from streamlit_gsheets import GSheetsConnection

# Create GSheets connection
st.title("Google Sheets as a DataBase")
def load_data():
    return conn.read(
        worksheet="Questões",  # Nome da planilha
        ttl="10m"                  # Cache de 10 minutos
    )
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
    existing_data = conn.read(worksheet="Questões")
    novo = pd.DataFrame({
        'Materia': [materia],
        'Descrição': [descricao],
        'Enunciado': [enunciado],
        'Alternativa_A': [letra_a],
        'Alternativa_B': [letra_b],
        'Alternativa_C': [letra_c],
        'Alternativa_D': [letra_d],
        'Alternativa_E': [letra_e]
    })
    
    combined_data = pd.concat([existing_data, novo], ignore_index=True)
    
    if st.button("Salvar"):   
    
        conn.update(worksheet="Questões", data=combined_data)
       
        updated_data = load_data()

        st.success("Questão salva")
        
    
