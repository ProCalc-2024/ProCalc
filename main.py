import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_option_menu import option_menu

def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            
local_css(r"styles.css")

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

authenticator.login()

if st.session_state["authentication_status"]:
    
    selected3 = option_menu(None, ["Home", "Save",  "Questions", 'Settings'], 
    icons=['house', 'cloud-upload', "list-task", 'gear'], 
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"margin":"0px", "--hover-color": "#868686"},
        "nav-link-selected": {"background-color": "black"},
    }
    )
    authenticator.logout()

elif st.session_state["authentication_status"] is False:
    st.error('O nome de usuário/senha está incorreto')
elif st.session_state["authentication_status"] is None:
    st.warning('Por favor insira seu nome de usuário e senha')

def new_senha():
    try:
        if authenticator.reset_password(st.session_state["username"]):
            st.success('Senha modificada com sucesso')
    except Exception as e:
        st.error(e)

def register_user():
    try:
        email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(pre_authorization=False)
        if email_of_registered_user:
            st.success('Usuário cadastrado com sucesso')
    except Exception as e:
        st.error(e)

with open('config.yaml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)
