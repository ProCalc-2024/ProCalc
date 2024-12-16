import streamlit as st

def read_questao():

   
    # Inicializa o estado da aba ativa no session_state
    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "Aba 1"
    
    # Define as abas e o índice com base no estado salvo
    tabs = ["Aba 1", "Aba 2", "Aba 3"]
    tab_index = tabs.index(st.session_state.active_tab)
    
    # Cria as abas
    selected_tab = st.tabs(tabs)[tab_index]
    
    # Atualiza o estado ao trocar de aba
    for i, tab in enumerate(tabs):
        if selected_tab == st.tabs[i]:
            st.session_state.active_tab = tab
    
    # Exibe conteúdo da aba selecionada
    if st.session_state.active_tab == "Aba 1":
        st.write("Conteúdo da Aba 1")
    elif st.session_state.active_tab == "Aba 2":
        st.write("Conteúdo da Aba 2")
    else:
        st.write("Conteúdo da Aba 3")
    
