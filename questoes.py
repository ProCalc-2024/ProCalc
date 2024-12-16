import streamlit as st

def read_questao():

   # Inicializa os estados
   if "auto_click" not in st.session_state:
       st.session_state.auto_click = False
   
   # Botão para acionar o "clique automático"
   if st.button("Ativar Clique Automático"):
       st.session_state.auto_click = True
   
   # Botão que será clicado automaticamente
   if st.session_state.auto_click:
       st.write("Clique automático ativado!")
   else:
       if st.button("Botão Simulado"):
           st.write("Você clicou manualmente no botão!")

