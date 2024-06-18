import streamlit as st
import database
    
with open("styles_save_ques.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

col1, col2, col3 = st.columns([1, 4, 1])
    
with col2 :

    st.title("Inserir Questões")

    with st.form("questao"):
        
        enunciao = st.text_area("Enunciado", placeholder= "digite aqui o enunciado da questão")
        respost1 = st.text_input("Resposta1", placeholder= "digite aqui a resposta correta")
        respost2 = st.text_input("Resposta2", placeholder= "digite aqui a resposta2")
        respost3 = st.text_input("Resposta3", placeholder= "digite aqui a resposta3")
        respost4 = st.text_input("Resposta4", placeholder= "digite aqui a resposta4")
        respost5 = st.text_input("Resposta5", placeholder= "digite aqui a resposta5")

        materia = database.read_materia()
        assunto = database.read_assunto()

        buton_login = st.form_submit_button("cadastrar")

        if buton_login:
            database.save_questao(enunciao, respost1, respost2, respost3, respost4, respost5)

        

        

    

            
