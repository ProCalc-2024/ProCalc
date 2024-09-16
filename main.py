import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Carregue as credenciais diretamente do secrets do Streamlit
credentials = Credentials.from_service_account_info(
    st.secrets["gsheets"]
)

# Autenticação e conexão com a planilha
client = gspread.authorize(credentials)

# Acesse a planilha
sheet = client.open("gsheets").sheet1

# Leia dados da planilha
df = sheet.get_all_records()

# Exiba os dados no Streamlit
st.write(df)

# Interface para entrada de novos dados
enunciado = st.text_input('Enunciado')
assunto = st.text_input('Assunto')

# Adicione nova linha na planilha quando clicar no botão
if st.button('Adicionar na planilha'):
    sheet.append_row([enunciado, assunto])
    st.success('Linha adicionada com sucesso!')
