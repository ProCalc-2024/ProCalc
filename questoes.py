import streamlit as st
import pandas as pd
import gspread
from streamlit_gsheets import GSheetsConnection
import numpy as np

def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            
local_css(r"styles_questao.css")

def read_questao():
    
    conn = st.connection("gsheets", type=GSheetsConnection)
    sheet = conn.read(worksheet="Questões")
    dict = pd.DataFrame(sheet)
    dict2 = dict.iloc[0]
    st.write(dict2["Alternativa_A"])
    
    col1, col2 = st.columns([1, 1])

    resul = {}

    # lista de materias
    lista = [ linha for linha in dict["Materia"]]

    with col2:    
        materia = st.selectbox("selecione um assunto",lista)    
    
    with col1:
        st.title("Perguntas")
    
    st.subheader('', divider = 'gray')
    
    #numero de questoes
    n=0
    
    for linha in dict["Materia"][materia]:
        n = n+1  

    # salvar as questoes de acordo com a materia escolhida 
    comando = dict["Materia"][materia]

    # embaralha as alternativas independente da questão 
    lista = [0,1,2,3,4]
    
    if "embaralho" not in st.session_state:
        
        st.session_state["embaralho"] = np.random.choice(lista, 5, replace = False)

    if "ques" not in st.session_state:
        st.session_state["save"] = {}
        st.session_state["numero"] = 0
        st.session_state["ques"] = np.random.randint(0,n)
         
    embaralho = st.session_state["embaralho"]
    
    # escolha de questão aleatoria
    Questão = st.session_state["ques"]

    # salva a questão aleatoria na variavel dic 
    dic = comando[list(comando)[Questão]]

    #comando da questão     
    st.write("")
    
    st.write(dic['enunciado'])
        
    st.subheader('', divider = 'gray')
    
    opções = [dic[list(dic)[embaralho[0]]], dic[list(dic)[embaralho[1]]],dic[list(dic)[embaralho[2]]], dic[list(dic)[embaralho[3]]], dic[list(dic)[embaralho[4]]]]    
    alternativa = st.radio("", options = opções)
        
    st.session_state["resposta"] = alternativa

    butao = st.button("Submeter") 
            
    # salva a sequencia de questoes
    resul.update(st.session_state["save"])
    
    st.session_state["save"] = { st.session_state["numero"] + 1 : st.session_state["ques"]                                                
                                                }

    questao = st.session_state["save"]

    resul.update(questao)
    
    # sequendcia de questões
    # st.write(resul)
    
    st.session_state["save"] = resul

    resposta = alternativa == dic[list(dic)[0]]

    if butao and resposta:         
        st.toast(':green-background[Resposta Certa]', icon='🎉')
        lis = [ lin for lin in resul ]
        new_ques(lista,n)
        st.rerun()

    elif butao and (resposta is False):
        st.toast(':red-background[Resposta Errada]', icon="⚠️")


def new_ques(lista,n):
    
    # salve as questões que foram feitas pelo usuario
    # so salvar questões que não foram feitas ainda 
    st.session_state["numero"] = st.session_state["numero"] + 1
    st.session_state["embaralho"] = np.random.choice(lista, 5, replace = False)
    st.session_state["ques"] =  np.random.randint(0,n)
    


         
