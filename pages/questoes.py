import streamlit as st
import database
import numpy as np

with open("styles_questao.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

col1, col2, col3 = st.columns([1, 4, 1])

lista = [2,3,4,5,6]
            
embaralho = np.random.choice(lista, 5, replace = False)


with col2 :
   
    resposta = database.read_questao(embaralho)
    


         