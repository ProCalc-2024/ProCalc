import streamlit as st

def read_questao():

   # Inicializa o estado no session_state
   if "active_tab" not in st.session_state:
       st.session_state.active_tab = 0  # Começa na primeira aba (índice 0)
   
   # Lista de abas
   tabs = ["Aba 1", "Aba 2", "Aba 3"]
   
   # Cria as abas e identifica qual aba está ativa
   tab_objects = st.tabs(tabs)
   
   # Mostra o conteúdo da aba automaticamente baseada no estado
   for i, tab in enumerate(tab_objects):
       with tab:
           if i == st.session_state.active_tab:
               st.write(f"Você está em: {tabs[i]}")
               st.session_state.active_tab = i  # Atualiza o índice caso algo seja alterado
   
   # Simula uma mudança automática no estado (exemplo: mudar para "Aba 2" após a renderização)
   # Isso pode ser adaptado conforme sua lógica de mudança automática
   if st.session_state.active_tab == 0:
       st.session_state.active_tab = 1  # Muda para a segunda aba automaticamente
   st.button("Say hello")
