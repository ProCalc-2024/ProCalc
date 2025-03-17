import streamlit as st

def ensino():

  # ID do vídeo do YouTube
  video_id = "dQw4w9WgXcQ"
  
  # Miniatura clicável que abre o vídeo diretamente no Streamlit
  st.markdown(
      f"""
      <a href="javascript:void(0);" onclick="document.getElementById('youtube_frame').src='https://www.youtube.com/embed/{video_id}?autoplay=1';">
          <img src="http://img.youtube.com/vi/{video_id}/0.jpg" width="560">
      </a>
      <br>
      <iframe id="youtube_frame" width="560" height="315" src="" frameborder="0" 
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; 
      gyroscope; picture-in-picture" allowfullscreen></iframe>
      """,
      unsafe_allow_html=True
  )

