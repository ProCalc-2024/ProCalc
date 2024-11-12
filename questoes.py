import streamlit as st
import pandas as pd
import gspread
from streamlit_gsheets import GSheetsConnection
import numpy as np
import time
import random

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css(r"styles_questao.css")

def read_questao():
    conn = st.connection("gsheets", type=GSheetsConnection)
    sheet = conn.read(worksheet="Questões")
    dict = pd.DataFrame(sheet)

    col1, col2, col3 = st.columns([1, 1, 1])
    test = {}
    resul = {}
    b = []
    evitar = []
    resposta = {}
    # lista de matérias
    lista = list(set(dict["Materia"]))
        
    with col2:    
        materia = st.selectbox("Selecione um assunto", lista)    

    # lista de questões de acordo com a matéria escolhida
    lista_ques = [linha for linha in dict.iloc if linha["Materia"] == materia]

    # Número de questões
    n = len(lista_ques)
    
    with col3:    
        # Pergunta ao usuário quantas questões deseja criar
        numero = st.number_input("Quantas questões você gostaria de fazer?", min_value=1, max_value=n, value=1)
        
    
    # Cria uma lista de nomes para as questões
    tab_names = [f"Q{i + 1}" for i in range(numero)]
    tab_names.append("Resposta")
    # Cria as abas dinamicamente
    tabs = st.tabs(tab_names)
     
    with tabs[numero]:
        col_list = [1] * numero
        coluna = st.columns(col_list)
    with col1:
        st.title("Perguntas")

    for i in range(numero):

        with tabs[i]:
            
            # Número de questões
            b = list(range(n))
            
            # Embaralha as alternativas
            lista = ["Alternativa_A", "Alternativa_B", "Alternativa_C", "Alternativa_D", "Alternativa_E"]
            if f"embaralho{i}" not in st.session_state:
                st.session_state[f"embaralho{i}"] = np.random.choice(lista, 5, replace=False)

            # Filtra os números que não estão na lista de exclusão
            opcoes_validas = [num for num in b if num not in evitar]
            opcoes_validas = list(set(opcoes_validas))

            if "ques" not in st.session_state:
                st.session_state["save"] = {}
                st.session_state["numero"] = 0
                random.shuffle(b)
                st.session_state["ques"] = b
            
            # se ja existir algo no sesion state 
            b = st.session_state["ques"]
            
            # Verifique se há opções válidas disponíveis
            if opcoes_validas:
                numero_aleatorio = np.random.choice(opcoes_validas)
           
            evitar.append(b[i])
            
            embaralho = st.session_state[f"embaralho{i}"]
            # Escolha de questão aleatória
            questao = lista_ques[b[i]]
            
            st.write(" ")
            st.write(questao["Enunciado"])
            st.subheader(' ', divider='gray')
            
            # Exibe as alternativas embaralhadas
            opcoes = [questao[embaralho[j]] for j in range(5)]
            
            alternativa = st.radio("", options=opcoes, index=None, key = f"key{i}")
            
            st.session_state["resposta"] = questao["Alternativa_A"]
            resul.update(st.session_state["save"])                                                
            st.session_state["save"] = {st.session_state["numero"] + 1: st.session_state["ques"]}
            sequencia = st.session_state["save"]
            resul.update(sequencia)
            st.session_state["save"] = resul
            resposta[i] = alternativa == questao["Alternativa_A"]
            if "botao" not in st.session_state:
               st.session_state["botao"] = False
        with tabs[numero]:

            botao = st.session_state["botao"]
           
            if botao is not True:
                x=0
                if alternativa is not None:
                            
                    index2 = opcoes.index(alternativa)
                    st.radio(tab_names[i], options=opcoes, index=index2, key=f"cha1{i}", disabled=True, horizontal=True) 
                    x = 1
                if x == 0:  
                    st.radio(tab_names[i], options=opcoes, index=None, key=f"cha2{i}", disabled=True, horizontal=True)
            if botao:
                x=0
                if resposta[i] == True:
                            
                    index2 = opcoes.index(alternativa)
                    st.radio(tab_names[i], options=opcoes, index=index2, key=f"cha1{i}", disabled=True, horizontal=True) 
                    st.success(f'A resposta correta e{questao["Alternativa_A"]}', icon="✅")
                    x = 1
                    
                if resposta[i] == False:  
                    st.radio(tab_names[i], options=opcoes, index=None, key=f"cha2{i}", disabled=True, horizontal=True)
                    st.error(f'A resposta correta e{questao["Alternativa_A"]}', icon="🚨")
     
    with tabs[numero]:
            # Botão de submissão
        st.session_state["botao"] = st.button("Submeter", key=f"sub{i}")  # Corrigido o espaço extra na chave


def new_ques(lista, n):
    # Salva as questões que foram feitas pelo usuário
    st.session_state["numero"] += 1
    st.session_state["embaralho"] = np.random.choice(lista, 5, replace=False)
    st.session_state["ques"] = np.random.randint(0, n)

