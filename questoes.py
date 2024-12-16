import streamlit as st

def read_questao():

   # Inicializa o estado da aba ativa
   if "active_tab" not in st.session_state:
       st.session_state.active_tab = "Aba 1"
   
   # Função para atualizar a aba ativa
   def set_tab(tab_name):
       st.session_state.active_tab = tab_name
   
   # Definição das abas
   tabs = ["Aba 1", "Aba 2", "Aba 3"]
   
   # Renderiza as abas com controle de estado
   selected_tab = st.radio("Escolha uma aba:", tabs, index=tabs.index(st.session_state.active_tab), horizontal=True, on_change=lambda: set_tab(st.session_state.active_tab))
   
   if selected_tab == "Aba 1":
       set_tab("Aba 1")
       st.write("Conteúdo da Aba 1")
   elif selected_tab == "Aba 2":
       set_tab("Aba 2")
       st.write("Conteúdo da Aba 2")
   elif selected_tab == "Aba 3":
       set_tab("Aba 3")
       st.write("Conteúdo da Aba 3")
