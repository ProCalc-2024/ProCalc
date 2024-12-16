import streamlit as st

def read_questao():

    # Inicializa o estado da aba selecionada no session_state
    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "Aba 1"
    
    # Função para mudar o estado da aba
    def change_tab(tab_name):
        st.session_state.active_tab = tab_name
    
    # Lista de abas
    tabs = ["Aba 1", "Aba 2", "Aba 3"]
    
    # Identifica a aba ativa
    active_tab = st.session_state.active_tab
    
    # Mostra as abas com controle do estado
    for tab in tabs:
        if st.button(tab):
            change_tab(tab)
            active_tab = tab
    
    # Mostra o conteúdo da aba ativa
    st.write(f"Você está em: {active_tab}")
    
    if active_tab == "Aba 1":
        st.write("Conteúdo da Aba 1")
    elif active_tab == "Aba 2":
        st.write("Conteúdo da Aba 2")
    elif active_tab == "Aba 3":
        st.write("Conteúdo da Aba 3")

