import streamlit as st 
from streamlit_option_menu import option_menu
import json
import os

# Caminho do arquivo para armazenar dados
DATA_FILE = "data.json"

# Função para carregar dados do arquivo
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

# CSS menu 
selected3 = option_menu(None, ["Home", "Save",  "Questions", 'Settings'], 
    icons=['house', 'cloud-upload', "list-task", 'gear'], 
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"margin":"0px", "--hover-color": "#868686"},
        "nav-link-selected": {"background-color": "black"},
    }
)

"-----------------------------------------------------"

# Função para salvar dados no arquivo
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# Carrega os dados do arquivo
data = load_data()

# Inicializa o texto salvo no session_state se não existir
if 'input_t' not in st.session_state:
    st.session_state.input_text = st

# Função para atualizar o texto e salvar
def update_text(entrada):
    st.session_state.input_text = entrada
    data['input_text'] = st.session_state.input_text
    save_data(data)

# Mostra o texto armazenado
st.write(f"Texto salvo: {st.session_state.input_text}")

entrada = st.radio("", options = [1, 2, 3, 4, 5])

bu = st.button('Incrementar')

if bu:
    update_text(entrada)

st.write(f"Texto salvo: {st.session_state.input_text}")
