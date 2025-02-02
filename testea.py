import streamlit as st
import pandas as pd
import gspread
from streamlit_gsheets import GSheetsConnection
import numpy as np

# Simulação de banco de dados de usuários (substituir por um banco real)
usuarios = {"admin": "1234", "user": "abcd"}  # login: senha

# Caixa de diálogo automática com login
def exibir_login():
    with st.modal("Login", closable=False):
        st.write("Por favor, faça login para continuar.")

        # Inputs de login
        usuario = st.text_input("Usuário", key="usuario")
        senha = st.text_input("Senha", type="password", key="senha")

        col1, col2 = st.columns(2)
        with col1:
            entrar = st.button("Entrar")
        with col2:
            cadastrar = st.button("Cadastrar-se")

        if entrar:
            if usuario in usuarios and usuarios[usuario] == senha:
                st.session_state["logado"] = True
                st.success("Login bem-sucedido! Bem-vindo, " + usuario)
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos!")

        if cadastrar:
            st.session_state["cadastro"] = True
            st.rerun()

# Caixa de diálogo para cadastro de usuário
def exibir_cadastro():
    with st.modal("Cadastro", closable=False):
        st.write("Crie sua conta para acessar o sistema.")

        novo_usuario = st.text_input("Novo Usuário", key="novo_usuario")
        nova_senha = st.text_input("Nova Senha", type="password", key="nova_senha")

        if st.button("Registrar"):
            if novo_usuario in usuarios:
                st.error("Usuário já existe! Tente outro nome.")
            elif novo_usuario and nova_senha:
                usuarios[novo_usuario] = nova_senha
                st.success("Cadastro realizado com sucesso! Faça login agora.")
                st.session_state["cadastro"] = False
                st.rerun()
            else:
                st.error("Preencha todos os campos!")

# Verifica se o usuário está logado
if "logado" not in st.session_state:
    st.session_state["logado"] = False

# Se estiver logado, exibe o conteúdo principal
if st.session_state["logado"]:
    st.write("🎉 Bem-vindo ao sistema!")
    if st.button("Sair"):
        st.session_state["logado"] = False
        st.rerun()
else:
    # Se não estiver cadastrado, exibe o login. Senão, exibe o cadastro.
    if st.session_state.get("cadastro", False):
        exibir_cadastro()
    else:
        exibir_login()
