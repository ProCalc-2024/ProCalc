import streamlit as st
import pandas as pd
import gspread
from streamlit_gsheets import GSheetsConnection
import numpy as np

def cadastrar_usuario():
    # Conexão com o Google Sheets
    conn = st.connection("gsheets", type=GSheetsConnection)
    sheet = conn.read(worksheet="Usuarios")
    df = pd.DataFrame(sheet)

    st.title("Cadastro de Usuário")

    # Campos de entrada para nome, e-mail e senha
    with st.form("cadastro_usuario"):
        nome = st.text_input("Nome:")
        email = st.text_input("E-mail:")
        senha = st.text_input("Senha:", type="password")
        confirmar_senha = st.text_input("Confirmar Senha:", type="password")
        submit_button = st.form_submit_button("Cadastrar")

    if submit_button:
        if senha != confirmar_senha:
            st.error("As senhas não coincidem. Tente novamente.")
        elif email in df["E-mail"].values:
            st.error("E-mail já cadastrado. Use outro e-mail.")
        else:
            novo_usuario = pd.DataFrame({"Nome": [nome], "E-mail": [email], "Senha": [senha]})
            df = pd.concat([df, novo_usuario], ignore_index=True)

            # Atualiza a planilha com os novos dados
            conn.update(worksheet="Usuarios", data=df)

            st.success("Usuário cadastrado com sucesso!")
