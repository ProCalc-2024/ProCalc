import mysql.connector
import streamlit as st
import numpy as np
import json
import os
import time



def create_login(usuario, email, senha):
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='#ProCalc2024',
        database='banco',
    )
    cursor = conexao.cursor()

    # CRUD

    comando = f'INSERT INTO usuario (Nome_User, Email_user, Senha_User) VALUES ("{usuario}", "{email}", "{senha}")'
    cursor.execute(comando)
    conexao.commit() # edita o banco de dados


    cursor.close()
    conexao.close()

def read_user(email, senha):
    
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
    
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='#ProCalc2024',
        database='banco',
    )
    cursor = conexao.cursor()

    # CRUD

    comando = f'SELECT * FROM usuario'
    cursor.execute(comando)
    linhas = cursor.fetchall() # ler o banco de dados

    for linha in linhas:

        if linha[2] == email and linha[3] == senha:
            st.write(linha[0], linha[1])


    cursor.close()
    conexao.close()

def save_questao(enunciado, resposta1, resposta2, resposta3, resposta4, resposta5):
    
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='#ProCalc2024',
        database='banco',
    )
    cursor = conexao.cursor()

    # CRUD

    comando = f'INSERT INTO questoes (enunciado, resposta1, resposta2, resposta3, resposta4, resposta5) VALUES ("{enunciado}", "{resposta1}", "{resposta2}", "{resposta3}", "{resposta4}", "{resposta5}")'
    cursor.execute(comando)
    conexao.commit() # edita o banco de dados


    cursor.close()
    conexao.close()

# Caminho do arquivo para armazenar dados
DATA_FILE = "data_1.json"

# Função para carregar dados do arquivo
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

# Função para salvar dados no arquivo
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)
    

# Carrega os dados do arquivo
data = load_data()

# Função para atualizar o texto e salvar
def update_1(embaralho):
        
    st.session_state.input_1 = embaralho
    data['input_1'] = st.session_state.input_1
    
    save_data(data)

def update_2(embaralho):
        
    st.session_state.input_2 = embaralho
    data['input_2'] = st.session_state.input_2
    
    save_data(data)

def update_3(embaralho):
        
    st.session_state.input_3 = embaralho
    data['input_3'] = st.session_state.input_3
    
    save_data(data)

def update_4(embaralho):
        
    st.session_state.input_4 = embaralho
    data['input_4'] = st.session_state.input_4
    
    save_data(data)

def update_5(embaralho):
        
    st.session_state.input_5 = embaralho
    data['input_5'] = st.session_state.input_5
    
    save_data(data)

def click_botao(alternativa, opções):

    update_1(opções[0])
    update_2(opções[1])
    update_3(opções[2])
    update_4(opções[3])
    update_5(opções[4])
 

def read_questao(embaralho):
    
    col1, col2, col3 = st.columns([1, 4, 1])
    
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='#ProCalc2024',
        database='banco',
    )
    cursor = conexao.cursor()

    # CRUD

    comando = f'SELECT * FROM questoes'
    cursor.execute(comando)
    linhas = cursor.fetchall() # ler o banco de dados

    n = 1

    # começar o json e adicionar as variaveis dentro dele 

    with st.form(linhas[n][1]):
        
        
        a = embaralho[0]
        b = embaralho[1]
        c = embaralho[2]
        d = embaralho[3]
        e = embaralho[4]

        if 'input_1' not in st.session_state:

            opções = [linhas[n][a], linhas[n][b], linhas[n][c], linhas[n][d], linhas[n][e]]
            
            st.session_state.input_1 = data.get('input_1', 1)
            st.session_state.input_2 = data.get('input_2', 2)
            st.session_state.input_3 = data.get('input_3', 3)
            st.session_state.input_4 = data.get('input_4', 4)
            st.session_state.input_5 = data.get('input_5', 5)

        st.write(linhas[n][1])
        st.subheader('', divider = 'gray')

        opções_antigo = opções.copy()

        opções = [linhas[n][a], linhas[n][b], linhas[n][c], linhas[n][d], linhas[n][e]]
        
        alternativa = st.radio("", options = opções, key = int(linhas[n][0])+22)
        st.write(alternativa)

        butao = st.form_submit_button("Submeter", on_click=click_botao(alternativa, opções_antigo)) 
        
        
        # não esta salvando oque eu estou selecionando pois ao apertar para verificar ele             
    
        resposta = alternativa == linhas[n][2]

        if butao and resposta:
                
            st.write("certo")
            time.sleep(2)          
        else:
            st.write("Errado")
    
    st.write(f"Texto salvo: {st.session_state.input_1}")
         
    cursor.close()
    conexao.close()

def create_materia(materia):
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='#ProCalc2024',
        database='banco',
    )
    cursor = conexao.cursor()

    # CRUD

    comando = f'INSERT INTO materia (materia) VALUES ("{materia}")'
    cursor.execute(comando)
    conexao.commit() # edita o banco de dados


    cursor.close()
    conexao.close()

def create_assunto(materia, assunto):
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='#ProCalc2024',
        database='banco',
    )
    cursor = conexao.cursor()

    # CRUD

    comando = f'INSERT INTO assunto (materia, assunto) VALUES ("{materia}", "{assunto}")'
    cursor.execute(comando)
    conexao.commit() # edita o banco de dados


    cursor.close()
    conexao.close()

def read_materia():

    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='#ProCalc2024',
        database='banco',
    )
    cursor = conexao.cursor()

    # CRUD

    comando = f'SELECT * FROM materia'
    cursor.execute(comando)
    linhas = cursor.fetchall() # ler o banco de dados

    lista = [ linha[1] for linha in linhas ]

    materia = st.selectbox("selecione uma materia", lista)

    cursor.close()
    conexao.close()

    return materia

def read_assunto():
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='#ProCalc2024',
        database='banco',
    )
    cursor = conexao.cursor()

    # CRUD

    comando = f'SELECT * FROM assunto'
    cursor.execute(comando)
    linhas = cursor.fetchall() # ler o banco de dados

    lista = [ linha[2] for linha in linhas ]

    assunto = st.text_input("descreva o assunto", placeholder= "assunto")

    cursor.close()
    conexao.close()

    return list 

# CREATE
# nome_produto = "chocolate"
# valor = 15
# comando = f'INSERT INTO vendas (nome_produto, valor) VALUES ("{nome_produto}", {valor})'
# cursor.execute(comando)
# conexao.commit() # edita o banco de dados


# READ
# comando = f'SELECT * FROM vendas'
# cursor.execute(comando)
# resultado = cursor.fetchall() # ler o banco de dados
# print(resultado)


# UPDATE
# nome_produto = "todynho"
# valor = 6
# comando = f'UPDATE vendas SET valor = {valor} WHERE nome_produto = "{nome_produto}"'
# cursor.execute(comando)
# conexao.commit() # edita o banco de dados

# DELETE
# nome_produto = "todynho"
# comando = f'DELETE FROM vendas WHERE nome_produto = "{nome_produto}"'
# cursor.execute(comando)
# conexao.commit() # edita o banco de dados
