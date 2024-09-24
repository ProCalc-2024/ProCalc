import streamlit as st
import pandas as pd
import gspread
from streamlit_gsheets import GSheetsConnection
import numpy as np
import time
def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            
local_css(r"styles_questao.css")

def read_questao():
    
    conn = st.connection("gsheets", type=GSheetsConnection)
    sheet = conn.read(worksheet="Questões")
    dict = pd.DataFrame(sheet)
    
    col1, col2 = st.columns([1, 1])

    resul = {}

    # lista de questões
    lista = list(set(dict["Materia"]))
        
    with col2:    
        materia = st.selectbox("selecione um assunto",lista)    

    # lista de questoes de acordo com a materia escolhida 
    lista_ques = []
    
    for linha in dict.iloc: 
        if linha["Materia"] == materia:
                lista_ques.append(linha)
        
    with col1:
        st.title("Perguntas")
    
    st.subheader('', divider = 'gray')
    
    #numero de questoes
    n=0
    for linha in lista_ques:
        n = n+1  

    # embaralha as alternativas independente da questão 
    lista = ["Alternativa_A","Alternativa_B","Alternativa_C","Alternativa_D","Alternativa_E"]
    
    if "embaralho" not in st.session_state:
        
        st.session_state["embaralho"] = np.random.choice(lista, 5, replace = False)

    if "ques" not in st.session_state:
        st.session_state["save"] = {}
        st.session_state["numero"] = 0
        st.session_state["ques"] = np.random.randint(0,n)
         
    embaralho = st.session_state["embaralho"]
    
    # escolha de questão aleatoria
    Questão = st.session_state["ques"]

    #comando da questão  
    questao = lista_ques[Questão]    
    st.write("")
    st.write(questao["Enunciado"])
        
    st.subheader('', divider = 'gray')
    
    opções = [questao[embaralho[0]], questao[embaralho[1]], questao[embaralho[2]], questao[embaralho[3]], questao[embaralho[4]]]    
    
    alternativa = st.radio("", options = opções)
        
    st.session_state["resposta"] = questao["Alternativa_A"]

    butao = st.button("Submeter") 
            
    # salva a sequencia de questoes
    resul.update(st.session_state["save"])                                                
    
    st.session_state["save"] = { st.session_state["numero"] + 1 : st.session_state["ques"] }
    
    sequencia = st.session_state["save"]
        
    resul.update(sequencia)

    # sequendcia de questões
    # st.write(resul)
    
    st.session_state["save"] = resul

    resposta = alternativa == questao["Alternativa_A"]

    if butao and resposta:         
        st.toast(':green-background[Resposta Certa]', icon='🎉')
        lis = [ lin for lin in resul ]
        new_ques(lista,n)
        time.sleep(5)
        st.rerun()

    elif butao and (resposta is False):
        st.toast(':red-background[Resposta Errada]', icon="⚠️")


def new_ques(lista,n):
    # salve as questões que foram feitas pelo usuario
    # so salvar questões que não foram feitas ainda 
    st.session_state["numero"] = st.session_state["numero"] + 1
    st.session_state["embaralho"] = np.random.choice(lista, 5, replace = False)
    st.session_state["ques"] =  np.random.randint(0,n)
    


         
