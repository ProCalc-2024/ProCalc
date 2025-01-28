import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Função para inserir um novo usuário na planilha
try:
    # Conexão com o Google Sheets
    conn = st.connection("gsheets", type=GSheetsConnection)
        
    # Leitura dos dados da planilha "Usuários"
    sheet_data = conn.read(worksheet="Usuários")
    df = pd.DataFrame(sheet_data)

    # Verificando se o e-mail já está cadastrado
    if email in df['Email'].values:
        st.warning("Este e-mail já está cadastrado!")
        return
        
    # Criando um novo registro
    novo_usuario = {
        "Nome": nome,
        "Email": email,
        "Senha": senha,
        "Tipo": tipo_usuario
    }
    # Adicionando o registro à planilha
    df = df.append(novo_usuario, ignore_index=True)
    conn.write(df, worksheet="Usuários")  # Salvando os dados na planilha
    st.success("Usuário cadastrado com sucesso!")
except Exception as e:
    st.error(f"Erro ao cadastrar usuário: {e}")

# Interface principal
st.title("Gerenciador de Usuários")
menu = st.sidebar.radio("Menu", ["Cadastro de Usuário", "Lista de Usuários"])

if menu == "Cadastro de Usuário":
    st.subheader("Cadastro de Novo Usuário")

    # Campos do formulário
    nome = st.text_input("Nome")
    email = st.text_input("E-mail")
    senha = st.text_input("Senha", type="password")
    tipo_usuario = "Usuário"  # Variável constante

    # Botão para cadastrar o usuário
    if st.button("Cadastrar"):
        if nome and email and senha:
            cadastrar_usuario(nome, email, senha, tipo_usuario)
        else:
            st.warning("Por favor, preencha todos os campos.")

elif menu == "Lista de Usuários":
    st.subheader("Lista de Usuários Cadastrados")
    try:
        # Conexão com o Google Sheets
        conn = st.connection("gsheets", type=GSheetsConnection)
        sheet_data = conn.read(worksheet="Usuários")
        df = pd.DataFrame(sheet_data)
        st.dataframe(df)
    except Exception as e:
        st.error(f"Erro ao acessar a planilha: {e}")
