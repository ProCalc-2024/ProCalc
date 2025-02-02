import streamlit as st
import pandas as pd
import gspread
from streamlit_gsheets import GSheetsConnection
import numpy as np

import streamlit as st

# Simulação de banco de dados de usuários (substituir por um banco real)
usuarios = {"admin": "1234", "user": "abcd"}  # login: senha

# Inicializa os estados
if "logado" not in st.session_state:
    st.session_state["logado"] = False
if "cadastro" not in st.session_state:
    st.session_state["cadastro"] = False
if "mostrar_modal" not in st.session_state:
    st.session_state["mostrar_modal"] = True  # Exibe o modal ao abrir

# Função para exibir login
def exibir_login():
    if hasattr(st, "experimental_dialog"):  # Se a versão do Streamlit for nova
        with st.experimental_dialog("Login"):
            login_form()
    else:  # Simulação com st.empty() para versões antigas
        modal = st.empty()
        with modal.container():
            login_form()
            if st.button("Fechar"):
                st.session_state["mostrar_modal"] = False
                modal.empty()

# Função para exibir o formulário de login
def login_form():
    st.write("Por favor, faça login para continuar.")
    usuario = st.text_input("Usuário", key="usuario")
    senha = st.text_input("Senha", type="password", key="senha")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Entrar"):
            if usuario in usuarios and usuarios[usuario] == senha:
                st.session_state["logado"] = True
                st.success("Login bem-sucedido! Bem-vindo, " + usuario)
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos!")
    with col2:
        if st.button("Cadastrar-se"):
            st.session_state["cadastro"] = True
            st.session_state["mostrar_modal"] = False
            st.rerun()

# Função para exibir cadastro
def exibir_cadastro():
    if hasattr(st, "experimental_dialog"):  # Se a versão do Streamlit for nova
        with st.experimental_dialog("Cadastro"):
            cadastro_form()
    else:
        modal = st.empty()
        with modal.container():
            cadastro_form()
            if st.button("Fechar"):
                st.session_state["cadastro"] = False
                modal.empty()

# Formulário de cadastro
def cadastro_form():
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
            st.session_state["mostrar_modal"] = True
            st.rerun()
        else:
            st.error("Preencha todos os campos!")

# Se o usuário não estiver logado, exibe o modal de login ou cadastro
if not st.session_state["logado"]:
    if st.session_state["cadastro"]:
        exibir_cadastro()
    elif st.session_state["mostrar_modal"]:
        exibir_login()
else:
    st.success("🎉 Bem-vindo ao sistema!")
    if st.button("Sair"):
        st.session_state["logado"] = False
        st.session_state["mostrar_modal"] = True
        st.rerun()

