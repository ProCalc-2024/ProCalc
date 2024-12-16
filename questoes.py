import streamlit as st

def read_questao():

    # Inicializar o estado da aba ativa
    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "Aba 1"  # Aba padrão inicial
    
    # Lista das abas disponíveis
    tabs = ["Aba 1", "Aba 2", "Aba 3"]
    
    # Criar botões ou links para simular o comportamento das abas
    selected_tab = st.radio("Selecione uma aba:", tabs, index=tabs.index(st.session_state.active_tab))
    
    # Atualizar o estado da aba ativa com base na seleção
    st.session_state.active_tab = selected_tab
    
    # Exibir o conteúdo da aba ativa
    if st.session_state.active_tab == "Aba 1":
        st.write("Você está na Aba 1!")
    elif st.session_state.active_tab == "Aba 2":
        st.write("Você está na Aba 2!")
    elif st.session_state.active_tab == "Aba 3":
        st.write("Você está na Aba 3!")

