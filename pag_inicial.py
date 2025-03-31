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
  
  # Inicializa o CookieManager uma vez por sessão

  # ✅ Inicializa o CookieManager UMA VEZ (evita recriação)
  if 'cookie_manager' not in st.session_state:
      st.session_state.cookie_manager = CookieManager(key="cookie_mgr")
  cookie_manager = st.session_state.cookie_manager
  
  # 🔍 Verifica se já está logado via cookie
  if 'user_logged_in' not in st.session_state:
      user_cookie = cookie_manager.get("user_auth")
      if user_cookie:
          st.session_state.user_logged_in = True
          st.session_state.username = user_cookie
      else:
          st.session_state.user_logged_in = False
  
  # 🔐 Página de Login
  if not st.session_state.user_logged_in:
      st.title("Login")
      username = st.text_input("Usuário")
      password = st.text_input("Senha", type="password")
  
      if st.button("Entrar"):
          if username == "admin" and password == "123":  # 👈 Simulação
              # 🍪 SALVA O COOKIE (com path e max_age)
              cookie_manager.set(
                  "user_auth",
                  username,
                  max_age=86400,  # 1 dia
                  path="/"
              )
              st.session_state.user_logged_in = True
              st.session_state.username = username
              st.experimental_rerun()  # 🔄 Recarrega para aplicar o cookie
          else:
              st.error("Credenciais inválidas")
  else:
      st.success(f"Bem-vindo, {st.session_state.username}!")
      if st.button("Sair"):
          cookie_manager.delete("user_auth")
          st.session_state.clear()
          st.experimental_rerun()
          

