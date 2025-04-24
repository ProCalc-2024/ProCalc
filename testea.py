import streamlit as st
import pandas as pd
import gspread
from streamlit_gsheets import GSheetsConnection
import numpy as np
from cryptography.fernet import Fernet
import time
import urllib.parse

def main():
    #Sistema de Login e Cadastro
    if "pagina" not in st.session_state:
        st.session_state["pagina"] = "Login"
        st.session_state["usuario"] = []

def cadastrar_usuario():
    chave = Fernet.generate_key()
    cipher = Fernet(chave)
    # Conexão com o Google Sheets
    conn = st.connection("gsheets", type=GSheetsConnection)
    sheet = conn.read(worksheet="Usuários", ttl=0)
    df = pd.DataFrame(sheet)

    st.subheader("Cadastro de Usuário")

    # Campos de entrada para nome, e-mail e senha
    with st.form("cadastro_usuario"):
        nome = st.text_input("Nome:")
        email = st.text_input("E-mail:")
        senha = st.text_input("Senha:", type="password")
        confirmar_senha = st.text_input("Confirmar Senha:", type="password")
        submit_button = st.form_submit_button("Cadastrar")
        Identificação = "Usuário"
        #st.write(f"Senha criptografada: {senha_encriptada}")
        
    if submit_button:
        # Validação
        if senha and len(senha) < 5:
            st.error("A senha deve ter pelo menos 6 caracteres!")
        elif senha != confirmar_senha:
            st.error("As senhas não coincidem. Tente novamente.")
        elif email in df["E-mail"].values:
            st.error("E-mail já cadastrado. Use outro e-mail.")
        else:
            novo_usuario = pd.DataFrame({"Nome": [nome], "E-mail": [email], "Identificação": [Identificação], "Senha": [senha]})
            df = pd.concat([df, novo_usuario], ignore_index=True)
            
            # Atualiza a planilha com os novos dados
            conn.update(worksheet="Usuários", data=df)

            conn.read(worksheet="Usuários", ttl=0)
            
            st.success("Usuário cadastrado com sucesso! Faça login agora.")
            
    if st.button("Ir para Login"):
        st.session_state["pagina"] = "Login"
        st.rerun()

def login_usuario():
    chave = Fernet.generate_key()
    cipher = Fernet(chave)
    # Conexão com o Google Sheets
    conn = st.connection("gsheets", type=GSheetsConnection)
    sheet = conn.read(worksheet="Usuários")
    df = pd.DataFrame(sheet)

    st.subheader("Login de Usuário")

    email = st.text_input("E-mail:")
    senha = st.text_input("Senha:", type="password")
    
    if st.button("Login"):
        if email in df["E-mail"].values:
            user_data = df[df["E-mail"] == email].iloc[0]
            
            if senha == user_data["Senha"]:
                st.toast(f':green-background[Login realizado com sucesso!]', icon='✅')
                st.session_state["usuario"] = user_data
                st.session_state["pagina"] = "Log"
                st.rerun()
                
            else:
                st.error("Senha incorreta. Tente novamente.")
        else:
            st.error("E-mail não encontrado.")
    
    if st.button("Cadastre-se"):
        st.session_state["pagina"] = "Cadastro"

        st.rerun()
    
    destinatario = "procalc14@gmail.com"
    subject = "Recuperação de Senha"
    body = "Olá,\n\nGostaria de solicitar a recuperação de senha para o e-mail associado à conta.\n\nAtenciosamente."
        
    # Codificar o assunto e corpo para garantir que os espaços e caracteres especiais sejam escapados
    subject_encoded = urllib.parse.quote(subject)
    body_encoded = urllib.parse.quote(body)
        
    # Gerar link para abrir o Gmail com o e-mail, assunto e corpo preenchidos
    gmail_link = f"https://mail.google.com/mail/?view=cm&fs=1&to={destinatario}&su={subject_encoded}&body={body_encoded}"
        
    # Exibir o link clicável com o texto apropriado
    st.info(f"Caso tenha esquecido sua senha, por gentileza, entre em contato através do e-mail: [Recuperação de Senha]({gmail_link})")
   
        
def aulas():
    
    conn = st.connection("gsheets", type=GSheetsConnection)
    sheet = conn.read(worksheet="Videos", ttl=0)
    df = pd.DataFrame(sheet)
    
    materias_unicas = df["Materia"].unique()
    
    lista = list(set(df["Materia"]))
    
    lista.sort()
    lista.insert(0, "Todas")
    
    #lista =  [linha for linha in df["Materia"]]
    
    materia = st.selectbox("Selecione um assunto:", lista)
    
    n_container = len(lista)-1
    
    if materia == "Todas":
        lista_ques = [linha for linha in df.iloc]
    else:
        lista_ques = [linha for linha in df.iloc if linha["Materia"] == materia]
    st.write(n)
    
    n_coluna = len(lista_ques)
    
    num_containers = 3
    num_colunas_por_container = 4
    
    for i in range(n_container):
        with st.container():
            st.subheader(f"Container {i+1}")
            
            # Cria as colunas dinamicamente
            colunas = st.columns(n_coluna)
    
            for j in range(n_coluna):
                with colunas[j]:
                    st.write(f"Container {i+1} - Coluna {j+1}")
                    st.button(f"Botão C{i+1} - Col{j+1}", key=f"btn_{i}_{j}")  
    
        
    
    
    
    
    
