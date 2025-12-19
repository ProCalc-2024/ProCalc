import streamlit as st
import pandas as pd
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
import pag_inicial

def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            
local_css(r"styles.css")

col1, col2, col3 = st.columns([1, 4, 1])

testea.main()

user = st.session_state["usuario"]

if st.session_state["pagina"] == "Login":
        testea.login_usuario()
if st.session_state["pagina"] == "Cadastro":
        testea.cadastrar_usuario()
if st.session_state["pagina"] == "Log":
    tab_names = []
    # Cria uma lista de nomes para as questões
    tab_names = ["Inicio", "Aulas", "Questionário", "Configurações"]
    if user["Identificação"] == "Administrador" or user["Identificação"] == "Moderador":   
            tab_names.append("Edição")
    # Cria as abas dinamicamente
    tabs = st.tabs(tab_names) 

    with col2:
        #with tabs[0]:        
        # Exibir a imagem no Streamlit
        # st.image("grafico.png", caption='Imagem do Google Drive')
        with tabs[0]:
                pag_inicial.ensino()
            
        if user["Identificação"] == "Administrador" or user["Identificação"] == "Moderador":      
                with tabs[4]:
                    co1, co2 = st.columns([1, 1])
        
                    with co1:
                # Adiciona "Editar Questões" como uma opção no selectbox
                        option = st.selectbox("", ("Adicionar Questões", "Adicionar Matérias", "Editar Questões", "Deletar Questão", "Inserir Video"), index=None, placeholder="Escolha uma ação")
        
                    match option:
                        case "Adicionar Questões":
                            save_questoes.inserir_ques()
                        case "Adicionar Matérias":
                            save_questoes.inserir_assun()
                        case "Editar Questões":
                            save_questoes.editar_ques()  # Chama a função para editar questões
                        case "Deletar Questão":
                            save_questoes.deletar_ques()
                        case "Inserir Video":
                            save_questoes.inserir_video()
                            pass
                with tabs[1]:
                    #testea.aulas()
                        # Centraliza tudo com markdown
                        st.markdown(
                            """
                            <div style="text-align: center; margin-top: 40px;">
                                <h1 style="font-size: 50px;">🚧 Em Construção 🚧</h1>
                                <p style="font-size: 24px;">Estamos trabalhando para trazer novidades em breve.</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

        else:
                with tabs[1]:

                        st.markdown(
                            """
                            <div style="text-align: center; margin-top: 100px;">
                                <h1 style="font-size: 60px;">🚧 Em Construção 🚧</h1>
                                <p style="font-size: 24px;">Estamos trabalhando para trazer novidades em breve.</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        
        with tabs[2]:
             
            questoes.read_questao()

        with tabs[3]:
            if st.button("logout"):
                    st.session_state["usuario"] = []
                    st.session_state["pagina"] = "Login"

                    st.rerun()
                    

