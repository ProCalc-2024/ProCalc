import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Conexão com Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read()

# Mostrar a tabela existente (Read)
st.write("Dados atuais:")
st.dataframe(df)

# Formulário para adicionar novos dados (Create)
st.write("Adicionar novo dado:")
with st.form("add_row_form"):
    enunciado = st.text_input("Enunciado")
    assunto = st.text_input("Assunto")
    if st.form_submit_button("Adicionar"):
        new_data = pd.DataFrame({
            "Enunciado": [enunciado],
            "Assunto": [assunto]
        })
        df = pd.concat([df, new_data], ignore_index=True)
        conn.write(df)  # Escreve de volta no Google Sheets
        st.success("Dado adicionado com sucesso!")
        st.experimental_rerun()  # Atualiza a página

# Seção para atualizar dados existentes (Update)
st.write("Atualizar dado existente:")
with st.form("update_row_form"):
    row_to_update = st.number_input("Número da linha para atualizar", min_value=0, max_value=len(df)-1)
    new_enunciado = st.text_input("Novo Enunciado", value=df.iloc[row_to_update]["Enunciado"])
    new_assunto = st.text_input("Novo Assunto", value=df.iloc[row_to_update]["Assunto"])
    if st.form_submit_button("Atualizar"):
        df.at[row_to_update, "Enunciado"] = new_enunciado
        df.at[row_to_update, "Assunto"] = new_assunto
        conn.write(df)  # Escreve de volta no Google Sheets
        st.success("Dado atualizado com sucesso!")
        st.experimental_rerun()  # Atualiza a página

# Seção para deletar dados (Delete)
st.write("Deletar dado:")
with st.form("delete_row_form"):
    row_to_delete = st.number_input("Número da linha para deletar", min_value=0, max_value=len(df)-1)
    if st.form_submit_button("Deletar"):
        df = df.drop(row_to_delete).reset_index(drop=True)  # Remove a linha e reseta os índices
        conn.write(df)  # Escreve de volta no Google Sheets
        st.success("Dado deletado com sucesso!")
        st.experimental_rerun()  # Atualiza a página


