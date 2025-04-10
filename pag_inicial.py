import streamlit as st
from extra_streamlit_components import CookieManager

def ensino():

  # URL do vídeo
  #video_url = "https://www.youtube.com/watch?v=d075cooe68s"

  # Exibir como link clicável (com miniatura do YouTube)
  #st.markdown(f'[![Assista no YouTube](http://img.youtube.com/vi/d075cooe68s/0.jpg)]({video_url})')

  #st.write("video_url")

  # Simulando um banco de dados de usuários
  
  # Inicializa o gerenciador de cookies
  
  # Inicializa o CookieManager uma vez por sessão

  # Inicializa o CookieManager UMA VEZ (evita recriação)
  # 1. Inicializa o CookieManager (SEMPRE no topo do script)
  st.markdown(
    """
    <div style="text-align: center; padding: 30px; background-color: #f0f2f6; border-radius: 15px;">
        <h2 style="color: #4B8BBE;">🚀 Bem-vindo ao <strong>Pro-Calc</strong>!</h2>
        <p style="font-size: 20px; color: #333;">
            <em>“Cada grande mente começou do zero – e você já deu um passo importante!”</em><br><br>
            O <strong>Pro-Calc</strong> está aqui para simplificar o <strong>pré-cálculo</strong> e te ajudar a evoluir a cada exercício.<br><br>
            <strong>Vamos juntos transformar desafios em conquistas! 💪📈</strong>
        </p>
    </div>
    """,
    unsafe_allow_html=True
  )
