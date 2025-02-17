import streamlit as st
import pandas as pd
import gspread
from streamlit_gsheets import GSheetsConnection
import numpy as np
from cryptography.fernet import Fernet
import time

def main():
    #Sistema de Login e Cadastro
    if "pagina" not in st.session_state:
        st.session_state["pagina"] = "Login"
        st.session_state["usuario"] = []
    
    if st.session_state["pagina"] == "Login":
        login_usuario()
    if st.session_state["pagina"] == "Cadastro":
        cadastrar_usuario()
    if st.session_state["pagina"] == "Log":
        oi()

if __name__ == "__main__":
    main()
def oi():
    st.write("oi")
def cadastrar_usuario():
    chave = Fernet.generate_key()
    cipher = Fernet(chave)
    # Conexão com o Google Sheets
    conn = st.connection("gsheets", type=GSheetsConnection)
    sheet = conn.read(worksheet="Usuários")
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
        senha_encriptada = cipher.encrypt(senha.encode())
        #st.write(f"Senha criptografada: {senha_encriptada}")
        
    if submit_button:
        if senha != confirmar_senha:
            st.error("As senhas não coincidem. Tente novamente.")
        elif email in df["E-mail"].values:
            st.error("E-mail já cadastrado. Use outro e-mail.")
        else:
            novo_usuario = pd.DataFrame({"Nome": [nome], "E-mail": [email], "Identificação": [Identificação], "Senha": [senha_encriptada]})
            df = pd.concat([df, novo_usuario], ignore_index=True)

            # Atualiza a planilha com os novos dados
            conn.update(worksheet="Usuários", data=df)

            conn.read(worksheet="Usuários", ttl="1s")
            
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
            sen = user_data["Senha"]
            
            
            if senha == user_data["Senha"]:
                st.toast(f':green-background[Login realizado com sucesso!]', icon='✅')
                st.session_state["usuario"] = user_data
                st.session_state["pagina"] == "Logado"
                st.rerun
                
            else:
                st.error("Senha incorreta. Tente novamente.")
        else:
            st.error("E-mail não encontrado.")
    
    st.write("Ainda não tem uma conta?")
    
    if st.button("Cadastre-se"):
        st.session_state["pagina"] = "Cadastro"

        st.rerun()
         
        
