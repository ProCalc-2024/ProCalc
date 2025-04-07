import streamlit as st
from streamlit_browser_cookie import get_cookie, set_cookie

def ensino():

    st.title("Cookie Demo")
    
    # Definindo um cookie (se ainda não estiver definido)
    if st.button("Definir cookie"):
        set_cookie("meu_cookie", "valor_do_cookie", max_age=3600)
        st.success("Cookie definido!")
    
    # Pegando o cookie
    cookie_valor = get_cookie("meu_cookie")
    
    if cookie_valor:
        st.info(f"Cookie encontrado: `{cookie_valor}`")
    else:
        st.warning("Nenhum cookie encontrado.")


