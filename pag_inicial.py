import streamlit as st

def ensino():

  # URL do vídeo
  video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  
  # Exibir como link clicável (com miniatura do YouTube)
  st.markdown(f'[![Assista no YouTube](http://img.youtube.com/vi/dQw4w9WgXcQ/0.jpg)]({video_url})')

