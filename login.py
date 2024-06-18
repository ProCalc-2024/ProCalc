import streamlit as st 
import database 

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

def Tela_login():
    
    col1, col2, col3 = st.columns([1, 4, 1])
    
    with col2:
        with st.form("lo1"):
            
            st.title("ProCalc")
        
            email = st.text_input("Email", placeholder= "digite aqui seu Email")
            senha = st.text_input("Senha", placeholder= "digite aqui sua Senha", type="password")
            
            st.write("")

            buton_login = st.form_submit_button("Logar", type="primary")

            if buton_login:
                database.read_user(email, senha)
            
            buton_cadastrar = st.form_submit_button("Cadastrar", type="primary")
            
            st.write(buton_cadastrar)

            return buton_cadastrar

            


def Tela_cadastro():
    
    col1, col2, col3 = st.columns([1, 4, 1])
    
    with col2:
        with st.form("lo2"):
           
            st.title("Registro")
        
            usuario = st.text_input("Nome", placeholder= "digite aqui seu Nome")
            email = st.text_input("Email", placeholder= "digite aqui seu Email")
            senha = st.text_input("Senha", placeholder= "digite aqui sua Senha", type="password")

            buton_cadastrar = st.form_submit_button("Cadastrar")

            if buton_cadastrar:
                database.create_login(usuario, email, senha)




