import streamlit as st
import pandas as pd
import gspread
from streamlit_gsheets import GSheetsConnection
import numpy as np
import time  # Importar para fazer a pausa de tempo

# Função para Adicionar Questões
def inserir_ques():    
    conn = st.connection("gsheets", type=GSheetsConnection)
    sheet = conn.read(worksheet="Materias")
    dict = pd.DataFrame(sheet)

    result = {}
    col1, col2 = st.columns([1, 1])
    lista = [linha for linha in dict["Materia"]]

    with col2:
        materia = st.selectbox("Selecione uma matéria", lista)

    with col1:
        descricao = st.text_input("Descrição")

    enunciado = st.text_area("Enunciado", placeholder="Digite aqui o enunciado da questão")
    letra_a = st.text_input("Resposta1", placeholder="Digite aqui a resposta correta")
    letra_b = st.text_input("Resposta2", placeholder="Digite aqui a resposta2")
    letra_c = st.text_input("Resposta3", placeholder="Digite aqui a resposta3")
    letra_d = st.text_input("Resposta4", placeholder="Digite aqui a resposta4")
    letra_e = st.text_input("Resposta5", placeholder="Digite aqui a resposta5")

    existing_data = conn.read(worksheet="Questões")
    novo = pd.DataFrame({
        'Materia': [materia],
        'Descrição': [descricao],
        'Enunciado': [enunciado],
        'Alternativa_A': [letra_a],
        'Alternativa_B': [letra_b],
        'Alternativa_C': [letra_c],
        'Alternativa_D': [letra_d],
        'Alternativa_E': [letra_e]
    })
    
    combined_data = pd.concat([existing_data, novo], ignore_index=True)

    if st.button("Salvar"):   
        conn.update(worksheet="Questões", data=combined_data)
        st.toast(':green-background[Questão salva]', icon='✔️')
        time.sleep(2)
        st.experimental_rerun()


# Função para Adicionar Materias
def inserir_assun():    
    conn = st.connection("gsheets", type=GSheetsConnection)
    existing = conn.read(worksheet="Materias")

    st.title("Novo Assunto")
    assun = st.text_area("Assunto", placeholder="Digite aqui o assunto")
    new = pd.DataFrame({'Materia': [assun]})
    
    combined = pd.concat([existing, new], ignore_index=True)
    
    if st.button("Salvar Assunto"):
        conn.update(worksheet="Materias", data=combined)
        st.toast(':green-background[Assunto salvo]', icon='✔️')
        time.sleep(2)
        st.experimental_rerun()


# Função para Editar Questões
def editar_ques():
    st.title("Editar Questões")
    
    conn = st.connection("gsheets", type=GSheetsConnection)
    existing_data = conn.read(worksheet="Questões")
    if existing_data.empty:
        st.warning("Nenhuma questão disponível para editar.")
        return
    
    questao_selecionada = st.selectbox("Selecione uma questão para editar", existing_data['Enunciado'])
    questao_atual = existing_data[existing_data['Enunciado'] == questao_selecionada].iloc[0]
    
    materia = st.selectbox("Matéria", options=existing_data["Materia"].unique(), index=existing_data["Materia"].tolist().index(questao_atual['Materia']))
    descricao = st.text_input("Descrição", value=questao_atual['Descrição'])
    enunciado = st.text_area("Enunciado", value=questao_atual['Enunciado'])
    letra_a = st.text_input("Resposta1", value=questao_atual['Alternativa_A'])
    letra_b = st.text_input("Resposta2", value=questao_atual['Alternativa_B'])
    letra_c = st.text_input("Resposta3", value=questao_atual['Alternativa_C'])
    letra_d = st.text_input("Resposta4", value=questao_atual['Alternativa_D'])
    letra_e = st.text_input("Resposta5", value=questao_atual['Alternativa_E'])
    
    if st.button("Salvar Alterações"):
        index = existing_data.index[existing_data['Enunciado'] == questao_selecionada][0]
        existing_data.at[index, 'Materia'] = materia
        existing_data.at[index, 'Descrição'] = descricao
        existing_data.at[index, 'Enunciado'] = enunciado
        existing_data.at[index, 'Alternativa_A'] = letra_a
        existing_data.at[index, 'Alternativa_B'] = letra_b
        existing_data.at[index, 'Alternativa_C'] = letra_c
        existing_data.at[index, 'Alternativa_D'] = letra_d
        existing_data.at[index, 'Alternativa_E'] = letra_e

        conn.update(worksheet="Questões", data=existing_data)
        st.toast(':green-background[Alterações salvas com sucesso]', icon='✔️')
        st.experimental_rerun()


# Barra lateral para navegação
st.sidebar.title("Menu")
aba_selecionada = st.sidebar.radio("Ir para:", ("Adicionar Questões", "Adicionar Materias", "Editar Questões"))

# Chama a função de acordo com a aba selecionada
if aba_selecionada == "Adicionar Questões":
    inserir_ques()
elif aba_selecionada == "Adicionar Materias":
    inserir_assun()
elif aba_selecionada == "Editar Questões":
    editar_ques()

