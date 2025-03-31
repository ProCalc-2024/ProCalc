import streamlit as st
from extra_streamlit_components import CookieManager

def ensino():

  # URL do vídeo
  #video_url = "https://www.youtube.com/watch?v=d075cooe68s"

  # Exibir como link clicável (com miniatura do YouTube)
  #st.markdown(f'[![Assista no YouTube](http://img.youtube.com/vi/d075cooe68s/0.jpg)]({video_url})')

  #st.video(video_url)

  # Simulando um banco de dados de usuários
  
  # Inicializa o gerenciador de cookies


  cookie_manager = CookieManager()
  
  # Verificar se o usuário já está logado (cookie existe)
  if 'user_logged_in' not in st.session_state:
      user_cookie = cookie_manager.get(cookie='user_auth')
      if user_cookie is not None:
          st.session_state.user_logged_in = True
          st.session_state.username = user_cookie
      else:
          st.session_state.user_logged_in = False
  
  # Página de login
  if not st.session_state.user_logged_in:
      username = st.text_input("Usuário")
      password = st.text_input("Senha", type="password")
      
      if st.button("Login"):
          if username == "admin" and password == "123":  # Simulação de autenticação
              st.session_state.user_logged_in = True
              st.session_state.username = username
              cookie_manager.set('user_auth', username, max_age=86400)  # Cookie válido por 1 dia
              st.rerun()
          else:
              st.error("Credenciais inválidas")
  else:
      st.success(f"Bem-vindo, {st.session_state.username}!")
      if st.button("Logout"):
          cookie_manager.delete('user_auth')
          st.session_state.clear()
          st.rerun()

        

