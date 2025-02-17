import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from cryptography.fernet import Fernet
import base64


CHAVE_FIXA = "8zMZjvwNYwKz9SoHCrneN_HoG072ha0Teq_Wo5lia5I="  
cipher = Fernet(CHAVE_FIXA)

def main():
    if "pagina" not in st.session_state:
        st.session_state["pagina"] = "Login"
    
    if st.session_state["pagina"] == "Login":
        login_usuario()
    else:
        cadastrar_usuario()

if __name__ == "__main__":
    main()

def cadastrar_usuario():
    conn = st.connection("gsheets", type=GSheetsConnection)
    sheet = conn.read(worksheet="Usuários")
    df = pd.DataFrame(sheet)

    st.subheader("Cadastro de Usuário")

    with st.form("cadastro_usuario"):
        nome = st.text_input("Nome:")
        email = st.text_input("E-mail:")
        senha = st.text_input("Senha:", type="password")
        confirmar_senha = st.text_input("Confirmar Senha:", type="password")
        submit_button = st.form_submit_button("Cadastrar")

    if submit_button:
        if senha != confirmar_senha:
            st.error("As senhas não coincidem. Tente novamente.")
        elif email in df["E-mail"].values:
            st.error("E-mail já cadastrado. Use outro e-mail.")
        else:
            senha_encriptada = cipher.encrypt(senha.encode()).decode()
            novo_usuario = pd.DataFrame({
                "Nome": [nome],
                "E-mail": [email],
                "Senha": [senha_encriptada]
            })
            df = pd.concat([df, novo_usuario], ignore_index=True)
            conn.update(worksheet="Usuários", data=df)
            st.success("Usuário cadastrado com sucesso! Faça login agora.")
            
    if st.button("Ir para Login"):
        st.session_state["pagina"] = "Login"
        st.rerun()

def login_usuario():
    conn = st.connection("gsheets", type=GSheetsConnection)
    sheet = conn.read(worksheet="Usuários")
    df = pd.DataFrame(sheet)

    st.subheader("Login de Usuário")

    email = st.text_input("E-mail:")
    senha = st.text_input("Senha:", type="password")
    
    if st.button("Login"):
        if email in df["E-mail"].values:
            user_data = df[df["E-mail"] == email].iloc[0]
            senha_criptografada = user_data["Senha"]
            
            try:
                senha_decifrada = cipher.decrypt(senha_criptografada.encode()).decode()
                if senha == senha_decifrada:
                    st.success("Login realizado com sucesso!")
                    st.session_state["usuario"] = user_data  # Define a chave "usuario"
                else:
                    st.error("Senha incorreta. Tente novamente.")
            except:
                st.error("Erro ao processar a senha. Tente novamente.")
        else:
            st.error("E-mail não encontrado.")
    
    if st.button("Cadastre-se"):
        st.session_state["pagina"] = "Cadastro"
        st.rerun()

    # Verifique se o usuário está autenticado antes de acessar a chave "usuario"
    if "usuario" in st.session_state and st.session_state["usuario"] is not None:
        st.write(f"Bem-vindo, {st.session_state['usuario']['Nome']}")
    else:
        st.warning("Por favor, faça login.")


