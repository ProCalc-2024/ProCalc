import streamlit as st 
import login
from streamlit_option_menu import option_menu
import streamlit as st
import streamlit_authenticator as stauth
import time

import streamlit as st

# Funções para cada página
def pagina_inicial():
    st.title("Página Inicial")
    st.write("Bem-vindo à Página Inicial!")

def pagina_sobre():
    st.title("Sobre")
    st.write("Esta é a página Sobre.")

def pagina_contato():
    st.title("Contato")
    st.write("Esta é a página de Contato.")

# Criar menu de navegação
paginas = {
    "Página Inicial": pagina_inicial,
    "Sobre": pagina_sobre,
    "Contato": pagina_contato
}

# Adicionar um seletor para o menu de navegação
escolha = st.sidebar.selectbox("Navegação", list(paginas.keys()))

# Executar a função da página selecionada
paginas[escolha]()

