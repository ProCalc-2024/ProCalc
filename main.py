import streamlit as st
import pandas as pd
import seaborn as sns
import gspread
from streamlit_gsheets import GSheetsConnection
import save_questoes as save_questoes
import questoes
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_option_menu import option_menu
from git import Repo
import requests


def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            
local_css(r"styles.css")

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

col1, col2, col3 = st.columns([1, 4, 1])

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

authenticator.login()

if st.session_state["authentication_status"]:
    
    tab1, tab2, tab3, tab4 = st.tabs([" Home", "Save", "Questions", "Settings"])

    with col2:
        
        co1, co2 = st.columns([1, 1])
            
        with tab2:
            with co1:
                if st.button("Inserir Questões"):    
                    save_questoes.inserir_ques()
            with co2:
                if st.button("Inserir Materias"):     
                    save_questoes.inserir_assun()

        with tab3:
            questoes.read_questao()

        with tab4:
            authenticator.logout()

        

elif st.session_state["authentication_status"] is False:
    st.error('O nome de usuário/senha está incorreto')
elif st.session_state["authentication_status"] is None:
    st.warning('Por favor insira seu nome de usuário e senha')

def new_senha():
    try:
        if authenticator.reset_password(st.session_state["username"]):
            st.success('Senha modificada com sucesso')
    except Exception as e:
        st.error(e)

def register_user():
    try:
        email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(pre_authorization=False)
        if email_of_registered_user:
            st.success('Usuário cadastrado com sucesso')
    except Exception as e:
        st.error(e)

with open('config.yaml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)
