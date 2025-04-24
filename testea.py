import streamlit as st
import pandas as pd
import gspread
from streamlit_gsheets import GSheetsConnection
import numpy as np
from cryptography.fernet import Fernet
import time
import urllib.parse

def main():
    #Sistema de Login e Cadastro
    if "pagina" not in st.session_state:
        st.session_state["pagina"] = "Login"
        st.session_state["usuario"] = []

def cadastrar_usuario():
    chave = Fernet.generate_key()
    cipher = Fernet(chave)
    # Conexão com o Google Sheets
    conn = st.connection("gsheets", type=GSheetsConnection)
    sheet = conn.read(worksheet="Usuários", ttl=0)
    df = pd.DataFrame(sheet)

    st.subheader("Cadastro de Usuário")

    # Campos de entrada para nome, e-mail e senha
    with st.form("cadastro_usuario"):
        nome = st.text_input("Nome:")
        email = st.text_input("E-mail:")
        senha = st.text_input("Senha:", type="password")
        confirmar_senha = st.text_input("Confirmar Senha:", type="password")
        submit_button = st.form_submit_button("Cadastrar")
        Identificação = "Usuário"
        #st.write(f"Senha criptografada: {senha_encriptada}")
        
    if submit_button:
        # Validação
        if senha and len(senha) < 5:
            st.error("A senha deve ter pelo menos 6 caracteres!")
        elif senha != confirmar_senha:
            st.error("As senhas não coincidem. Tente novamente.")
        elif email in df["E-mail"].values:
            st.error("E-mail já cadastrado. Use outro e-mail.")
        else:
            novo_usuario = pd.DataFrame({"Nome": [nome], "E-mail": [email], "Identificação": [Identificação], "Senha": [senha]})
            df = pd.concat([df, novo_usuario], ignore_index=True)
            
            # Atualiza a planilha com os novos dados
            conn.update(worksheet="Usuários", data=df)

            conn.read(worksheet="Usuários", ttl=0)
            
            st.success("Usuário cadastrado com sucesso! Faça login agora.")
            
    if st.button("Ir para Login"):
        st.session_state["pagina"] = "Login"
        st.rerun()

def login_usuario():
    chave = Fernet.generate_key()
    cipher = Fernet(chave)
    # Conexão com o Google Sheets
    conn = st.connection("gsheets", type=GSheetsConnection)
    sheet = conn.read(worksheet="Usuários")
    df = pd.DataFrame(sheet)

    st.subheader("Login de Usuário")

    email = st.text_input("E-mail:")
    senha = st.text_input("Senha:", type="password")
    
    if st.button("Login"):
        if email in df["E-mail"].values:
            user_data = df[df["E-mail"] == email].iloc[0]
            
            if senha == user_data["Senha"]:
                st.toast(f':green-background[Login realizado com sucesso!]', icon='✅')
                st.session_state["usuario"] = user_data
                st.session_state["pagina"] = "Log"
                st.rerun()
                
            else:
                st.error("Senha incorreta. Tente novamente.")
        else:
            st.error("E-mail não encontrado.")
    
    if st.button("Cadastre-se"):
        st.session_state["pagina"] = "Cadastro"

        st.rerun()
    
    destinatario = "procalc14@gmail.com"
    subject = "Recuperação de Senha"
    body = "Olá,\n\nGostaria de solicitar a recuperação de senha para o e-mail associado à conta.\n\nAtenciosamente."
        
    # Codificar o assunto e corpo para garantir que os espaços e caracteres especiais sejam escapados
    subject_encoded = urllib.parse.quote(subject)
    body_encoded = urllib.parse.quote(body)
        
    # Gerar link para abrir o Gmail com o e-mail, assunto e corpo preenchidos
    gmail_link = f"https://mail.google.com/mail/?view=cm&fs=1&to={destinatario}&su={subject_encoded}&body={body_encoded}"
        
    # Exibir o link clicável com o texto apropriado
    st.info(f"Caso tenha esquecido sua senha, por gentileza, entre em contato através do e-mail: [Recuperação de Senha]({gmail_link})")
   
        
def aulas():

    # Conexão com Google Sheets
    conn = st.connection("gsheets", type=GSheetsConnection)
    sheet = conn.read(worksheet="Videos", ttl=0)
    df = pd.DataFrame(sheet)
    
    # Lista de matérias únicas
    materias = df["Materia"].dropna().unique().tolist()
    materias.sort()
    materias.insert(0, "Todas")
    
    # Filtro
    materia_selecionada = st.selectbox("Selecione um assunto:", materias)
    
    # Filtragem de dados
    if materia_selecionada == "Todas":
        materias_dict = {
            mat: df[df["Materia"] == mat].to_dict(orient="records")
            for mat in df["Materia"].unique()
        }
    else:
        materias_dict = {
            materia_selecionada: df[df["Materia"] == materia_selecionada].to_dict(orient="records")
        }
    
    # Estilo para scroll lateral
    st.markdown("""
        <style>
            .video-scroll {
                display: flex;
                overflow-x: auto;
                padding: 10px 0;
            }
            .video-card {
                flex: 0 0 auto;
                width: 220px;
                margin-right: 16px;
                text-align: center;
            }
            .video-card img {
                width: 100%;
                border-radius: 8px;
            }
            .video-title {
                font-size: 14px;
                font-weight: bold;
                margin-top: 5px;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Renderização dos vídeos
    for materia, videos in materias_dict.items():
        if not videos:
            continue
    
        st.markdown(f"### 🎓 {materia}")
        html_cards = '<div class="video-scroll">'
    
        for video in videos:
            link = video.get("Link", "")
            titulo = video.get("Titulo", "Sem título")
    
            if "v=" in link:
                video_id = link.split("v=")[-1].split("&")[0]
                thumbnail_url = f"http://img.youtube.com/vi/{video_id}/0.jpg"
    
                html_cards += f"""
                    <div class="video-card">
                        <a href="{link}" target="_blank">
                            <img src="{thumbnail_url}" alt="{titulo}">
                            <div class="video-title">{titulo}</div>
                        </a>
                    </div>
                """
        html_cards += '</div>'
        st.markdown(html_cards, unsafe_allow_html=True)
