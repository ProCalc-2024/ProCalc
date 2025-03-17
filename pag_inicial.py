import streamlit as st

def ensino():
  st.title("Vídeo do YouTube no Streamlit")
  
  # URL do vídeo
  video_url = "https://youtu.be/3rxEC_TOfj8?si=Jc0r2CHQEgRjyabE"
  
  # Exibir como link clicável (com miniatura do YouTube)
  st.markdown(f'[![Assista no YouTube](https://youtu.be/3rxEC_TOfj8?si=Jc0r2CHQEgRjyabE/0.jpg)]({video_url})')
