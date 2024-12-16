import streamlit as st

def read_questao():

   # Inicializa o estado da aba ativa
   if "active_tab" not in st.session_state:
       st.session_state.active_tab = 0  # Começa na Aba 1
   
   # Criação das abas
   tab1, tab2, tab3 = st.tabs(["Aba 1", "Aba 2", "Aba 3"])
   
   # Função para manter a aba ativa
   def set_active_tab(index):
       st.session_state.active_tab = index
   
   # Renderização do conteúdo de acordo com a aba ativa
   if st.session_state.active_tab == 0:
       with tab1:
           st.write("Conteúdo da Aba 1")
           set_active_tab(0)
   
   if st.session_state.active_tab == 1:
       with tab2:
           st.write("Conteúdo da Aba 2")
           set_active_tab(1)
   
   if st.session_state.active_tab == 2:
       with tab3:
           st.write("Conteúdo da Aba 3")
           set_active_tab(2)
   st.button("Say hello")       
