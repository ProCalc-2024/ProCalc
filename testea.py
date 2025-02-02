import streamlit as st
import pandas as pd
import gspread
from streamlit_gsheets import GSheetsConnection
import numpy as np

def inserir_usuario():   

    container = st.container(border=True)
    
    conn = st.connection("gsheets", type=GSheetsConnection)
    sheet = conn.read(worksheet="Usuários")
    dict = pd.DataFrame(sheet)
    # adicionar uma nova pergunta
    result = {}
    
    col1, col2 = st.columns([1, 1])

    lista =  [linha for linha in dict["Nome"]]
    
    Nome_user = st.text_input("Nome do Usuário", placeholder= "digite aqui seu Nome", key = "Nome_user") 
    Email_user = st.text_input("Email do Usuário", placeholder= "digite aqui seu Email", key = "Email_user")
    Senha_user = st.text_input("Senha do Usuario", placeholder= "digite aqui sua senha", key = "Senha_user") 
    id_user = "Usuário" 

    existing_data = conn.read(worksheet="Usuários")
    novo = pd.DataFrame({
        'Nome': [Nome_user],
        'Email': [Email_user],
        'Senha': [Senha_user],
        'Identificação': [id_user]
    })
    
    combined_data = pd.concat([existing_data, novo], ignore_index=True)
    st.write(combined_data)        
                
    #st.toast(':green-background[Resposta Certa]', icon='🎉')
    
    #st.toast(':red-background[Resposta Errada]', icon="⚠️")
        
    if st.button("Cadastrar-se"):   
        
            
        conn.update(worksheet="Usuários", data=combined_data)
       
        conn.read(
        worksheet="Usuários",  # Nome da planilha
        ttl="1s"                  # Cache de 10 minutos
        )
        
        st.success(':green-background[Questão salva]', icon='✔️')
        
        st.rerun()

