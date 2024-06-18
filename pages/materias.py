import streamlit as st
import database

with open("styles_save_ques.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

col1, col2 = st.columns([1, 1])
    
with col1 :

    st.title("Inserir materia")

    with st.form("save_materia"):
        
        materia = st.text_input("materia", placeholder= "digite aqui a materia")

        buton_materia = st.form_submit_button("Cadastrar Questão", type = "primary")

        if buton_materia:
            database.create_materia(materia)

with col2 :

    st.title("Inserir Assunto")

    with st.form("save_assunto"):
        
        materia = database.read_materia()

        assunto = st.text_input("assunto", placeholder = "digite aqui a assunto")

        st.write("")

        buton_login = st.form_submit_button("Cadastrar materia", type = "primary")

        if buton_login:
            database.create_assunto(materia, assunto)