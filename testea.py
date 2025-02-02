import streamlit as st
import pandas as pd
import gspread
from streamlit_gsheets import GSheetsConnection
import numpy as np

import streamlit as st

import streamlit as st

# Simulação de banco de dados de usuários
usuarios = {"admin": "1234", "user": "abcd"}

# Gerenciando o estado do modal
if "mostrar_modal" not in st.session_state:
    st.session_state.mostrar_modal = True  # Inicia mostrando o modal
if "cadastro" not in st.session_state:
    st.session_state.cadastro = False

def fechar_modal():
    st.session_state.mostrar_modal = False
    st.rerun()

def abrir_cadastro():
    st.session_state.cadastro = True
    st.rerun()

def fechar_cadastro():
    st.session_state.cadastro = False
    st.rerun()

# Se o usuário estiver logado, exibe o conteúdo
if "logado" not in st.session_state:
    st.session_state["logado"] = False

if st.session_state["logado"]:
    st.success("🎉 Bem-vindo ao sistema!")
    if st.button("Sair"):
        st.session_state["logado"] = False
        st.rerun()
else:
    if st.session_state.mostrar_modal:
        modal = st.empty()
        with modal.container():
            st.write("### Login")
            usuario = st.text_input("Usuário")
            senha = st.text_input("Senha", type="password")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Entrar"):
                    if usuario in usuarios and usuarios[usuario] == senha:
                        st.session_state["logado"] = True
                        fechar_modal()
                    else:
                        st.error("Usuário ou senha incorretos!")

            with col2:
                if st.button("Cadastrar-se"):
                    abrir_cadastro()

    if st.session_state.cadastro:
        modal = st.empty()
        with modal.container():
            st.write("### Cadastro")
            novo_usuario = st.text_input("Novo Usuário")
            nova_senha = st.text_input("Nova Senha", type="password")

            if st.button("Registrar"):
                if novo_usuario in usuarios:
                    st.error("Usuário já existe! Tente outro nome.")
                elif novo_usuario and nova_senha:
                    usuarios[novo_usuario] = nova_senha
                    st.success("Cadastro realizado! Faça login.")
                    fechar_cadastro()
                else:
                    st.error("Preencha todos os campos!")


