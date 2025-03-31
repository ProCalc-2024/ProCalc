import streamlit as st
import streamlit_cookies_manager

def ensino():

  # URL do vídeo
  #video_url = "https://www.youtube.com/watch?v=d075cooe68s"

  # Exibir como link clicável (com miniatura do YouTube)
  #st.markdown(f'[![Assista no YouTube](http://img.youtube.com/vi/d075cooe68s/0.jpg)]({video_url})')

  #st.video(video_url)

  # Simulando um banco de dados de usuários
  
  # Inicializa o gerenciador de cookies
  cookies = streamlit_cookies_manager.CookieManager()
  
  # Simulação de um banco de usuários
  USERS = {"leandro": "1234", "admin": "senha"}
  
  # Verifica se já há um cookie de login
  if cookies.ready():
      login_cookie = cookies.get("login_token")
      if login_cookie:
          st.session_state.logged_in = True
          st.session_state.username = login_cookie
  
  # Se não estiver autenticado, exibir tela de login
  if "logged_in" not in st.session_state or not st.session_state.logged_in:
      st.title("Login")
      username = st.text_input("Usuário")
      password = st.text_input("Senha", type="password")
  
      if st.button("Entrar"):
          if username in USERS and USERS[username] == password:
              st.session_state.logged_in = True
              st.session_state.username = username
              cookies.set("login_token", username, expires_at="2025-12-31T23:59:59Z")  # Cookie expira no futuro
              st.experimental_rerun()
          else:
              st.error("Usuário ou senha incorretos!")
  
  # Se estiver autenticado, mostrar conteúdo
  if st.session_state.get("logged_in", False):
      st.success(f"Bem-vindo, {st.session_state.username}!")
  
      if st.button("Sair"):
          cookies.delete("login_token")  # Remove o cookie
          st.session_state.logged_in = False
          st.experimental_rerun()

        

