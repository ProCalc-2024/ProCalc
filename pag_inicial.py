import streamlit as st

def ensino():

  if "clicked" not in st.session_state:
      st.session_state.clicked = False
  
  # HTML para criar um link clicável que atualiza a sessão
  st.markdown(
      """
      <a href="?run=1" target="_self">
          <img src="http://img.youtube.com/vi/dQw4w9WgXcQ/0.jpg" width="560">
      </a>
      """,
      unsafe_allow_html=True
  )
  
  # Detectar se a URL contém "run=1" (simula um clique)
  query_params = st.query_params
  if "run" in query_params:
      st.session_state.clicked = True
      st.experimental_rerun()
  
  # Exibir vídeo se foi clicado
  if st.session_state.clicked:
      st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
