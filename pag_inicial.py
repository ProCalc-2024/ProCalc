import streamlit as st
from streamlit_js_eval import get_local_storage, set_local_storage, clear_local_storage

def ensino():

  # URL do vídeo
  #video_url = "https://www.youtube.com/watch?v=d075cooe68s"

  # Exibir como link clicável (com miniatura do YouTube)
  #st.markdown(f'[![Assista no YouTube](http://img.youtube.com/vi/d075cooe68s/0.jpg)]({video_url})')

  #st.video(video_url)

  # Simulando um banco de dados de usuários
  USERS = {"leandro": "1234", "admin": "senha"}
  
  # Checar se já existe um token de login salvo
  token = get_local_storage("login_token")
  
  if token and "logged_in" not in st.session_state:
      st.session_state.logged_in = True
      st.session_state.username = token
  
  # Se não estiver autenticado, exibir tela de login
  if "logged_in" not in st.session_state or not st.session_state.logged_in:
      st.title("Login")
      username = st.text_input("Usuário")
      password = st.text_input("Senha", type="password")
  
      if st.button("Entrar"):
          if username in USERS and USERS[username] == password:
              st.session_state.logged_in = True
              st.session_state.username = username
              set_local_storage("login_token", username)  # Salva no navegador
              st.experimental_rerun()
          else:
              st.error("Usuário ou senha incorretos!")
  
  # Se estiver autenticado, mostrar conteúdo
  if st.session_state.get("logged_in", False):
      st.success(f"Bem-vindo, {st.session_state.username}!")
  
      if st.button("Sair"):
          clear_local_storage("login_token")  # Remove do navegador
          st.session_state.logged_in = False
          st.experimental_rerun()
        

