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
import testea


def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            
local_css(r"styles.css")

col1, col2, col3 = st.columns([1, 4, 1])

testea.main()

if st.session_state["pagina"] == "Login":
        testea.login_usuario()
if st.session_state["pagina"] == "Cadastro":
        testea.cadastrar_usuario()

log = st.session_state["pagina"]
user = st.session_state["usuario"]
st.write(log)
if st.session_state["pagina"] == "Log":
    tab_names = []
    # Cria uma lista de nomes para as questões
    tab_names = ["Inicio", "Questionario", "Configurações"]
           
    tab_names.append("Edição")
    # Cria as abas dinamicamente
    tabs = st.tabs(tab_names) 

    with col2:
        #with tabs[0]:
                

                        
                # Exibir a imagem no Streamlit
                # st.image("grafico.png", caption='Imagem do Google Drive')
            
        with tabs[3]:
            co1, co2 = st.columns([1, 1])

            with co1:
        # Adiciona "Editar Questões" como uma opção no selectbox
                option = st.selectbox("", ("Adicionar Questões", "Adicionar Materias", "Editar Questões", "Deletar Questão"), 
                              index=None, placeholder="Escolha uma ação")

            match option:
                case "Adicionar Questões":
                    save_questoes.inserir_ques()
                case "Adicionar Materias":
                    save_questoes.inserir_assun()
                case "Editar Questões":
                    save_questoes.editar_ques()  # Chama a função para editar questões
                case "Deletar Questão":
                    save_questoes.deletar_ques()
                    pass
        with tabs[1]:
             
            questoes.read_questao()

        with tabs[2]:
            st.button("logout")
                    
