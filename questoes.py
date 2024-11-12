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
    res = {}

    if "botao" not in st.session_state:
        st.session_state["botao"] = False
        st.session_state["disabled"] = False
            
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
            
            disabled2 = st.session_state["disabled"]
            
            # Embaralha as alternativas
            lista = ["Alternativa_A", "Alternativa_B", "Alternativa_C", "Alternativa_D", "Alternativa_E"]
            if f"embaralho{i}{materia}" not in st.session_state:
                st.session_state[f"embaralho{i}{materia}"] = np.random.choice(lista, 5, replace=False)

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
            
            embaralho = st.session_state[f"embaralho{i}{materia}"]
            # Escolha de questão aleatória
            questao = lista_ques[b[i]]
            
            st.write(" ")
            st.write(questao["Enunciado"])
            st.subheader(' ', divider='gray')
            
            # Exibe as alternativas embaralhadas
            opcoes = [questao[embaralho[j]] for j in range(5)]
            
            alternativa = st.radio("", options=opcoes, index=None, key = f"key{i}", disabled=disabled2)
            
            st.session_state["resposta"] = questao["Alternativa_A"]
            resul.update(st.session_state["save"])                                                
            st.session_state["save"] = {st.session_state["numero"] + 1: st.session_state["ques"]}
            sequencia = st.session_state["save"]
            resul.update(sequencia)
            st.session_state["save"] = resul
            resposta[i] = alternativa == questao["Alternativa_A"]
            

                
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
            if botao and alternativa is not None:
                
                index2 = opcoes.index(alternativa)
                st.radio(tab_names[i], options=opcoes, index=index2, key=f"cha3{i}", disabled=True, horizontal=True) 
                
                if resposta[i] == True:
                            
                    st.success(f'A resposta correta e {questao["Alternativa_A"]}', icon="✅")
             
                if resposta[i] == False:  
            
                    st.error(f'A resposta correta e {questao["Alternativa_A"]}', icon="🚨")
                res[i] = True
                
            if botao and alternativa is None:
                st.radio(tab_names[i], options=opcoes, index=None, key=f"cha4{i}", disabled=True, horizontal=True)
                st.warning('Nenhuma das alternativas foi selecionada.', icon="⚠️")
                res[i] = False
                
                st.write(res[i])

    res2 = list(set(res))
    st.write(res2)
    with tabs[numero]:
        def click1():
            if not st.session_state["botao"] :
                if st.button("Submeter", on_click=clicar_botao,key = "botao2"):
                    pass  # O estado muda ao clicar, e o botão desaparece na próxima renderização            
        
        def clicar_botao():
            st.session_state["botao"] = True
            st.session_state["disabled"] = True

        def new_questionario():
            st.session_state["botao"] = None
            st.session_state["disabled"] = False
            
        # Mostra o botão somente se ele ainda não foi clicado
        if not st.session_state["botao"] :
            if st.button("Submeter", on_click=click1, key = "botao1"):
                pass  # O estado muda ao clicar, e o botão desaparece na próxima renderização

        if st.session_state["botao"] :       
            if st.button("Novas Perguntas", on_click=new_questionario):
                pass  # O estado muda ao clicar, e o botão desaparece na próxima renderização
        
        # Define a variável com base no estado do botão
        botao = st.session_state["botao"]

# Função que será chamada ao clicar no botão


def new_ques(lista, n):
    # Salva as questões que foram feitas pelo usuário
    st.session_state["numero"] += 1
    st.session_state["embaralho"] = np.random.choice(lista, 5, replace=False)
    st.session_state["ques"] = np.random.randint(0, n)

