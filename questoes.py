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
    dict_df = pd.DataFrame(sheet)
    
    col1, col2, col3 = st.columns([1, 1, 1])

    # Lista de matérias para seleção do usuário
    materias_lista = sorted(list(set(dict_df["Materia"])))
    
    # Controle da seleção de matéria
    if "materia_anterior" not in st.session_state:
        st.session_state["materia_anterior"] = None
    
    with col2:
        materia = st.selectbox("Selecione um assunto", materias_lista)
    
    # Reseta as questões respondidas e o embaralhamento se a matéria mudar
    if st.session_state["materia_anterior"] != materia:
        st.session_state["respondidas"] = set()
        st.session_state["embaralho"] = np.random.permutation(["Alternativa_A", "Alternativa_B", "Alternativa_C", "Alternativa_D", "Alternativa_E"])
        st.session_state["materia_anterior"] = materia
    
    # Filtra questões da matéria selecionada
    questoes_materia = dict_df[dict_df["Materia"] == materia].to_dict(orient='records')
    
    with col3:    
        # Pergunta ao usuário quantas questões deseja responder
        numero = st.number_input("Quantas Questões você gostaria de fazer?", min_value=1, max_value=min(20, len(questoes_materia)), value=1)
    
    # Cria as abas dinamicamente
    tab_names = [f"Q{i + 1}" for i in range(numero)]
    tabs = st.tabs(tab_names)
    
    with col1:
        st.title("Perguntas")

    resultados = {}
    
    for i in range(numero):
        with tabs[i]:
            questao = selecionar_questao(questoes_materia)
            st.write('')
            st.write(questao["Enunciado"])

            # Embaralha as alternativas
            alternativas_embaralhadas = [questao[alt] for alt in st.session_state["embaralho"]]
            resposta_correta = questao["Alternativa_A"]

            # Exibe alternativas
            alternativa_escolhida = st.radio("Escolha a alternativa correta:", options=alternativas_embaralhadas, key=f"alternativa_{i}")
            resultados[f"Q{i+1}"] = (alternativa_escolhida, resposta_correta)
    
    if st.button("Submeter"):
        verificar_respostas(resultados)

def selecionar_questao(questoes_materia):
    # Seleciona uma questão que ainda não foi respondida
    opcoes_validas = [q for idx, q in enumerate(questoes_materia) if idx not in st.session_state["respondidas"]]
    
    if opcoes_validas:
        questao_selecionada = np.random.choice(opcoes_validas)
        st.session_state["respondidas"].add(questoes_materia.index(questao_selecionada))
        return questao_selecionada
    else:
        st.write("Você respondeu todas as perguntas dessa matéria!")
        st.stop()

def verificar_respostas(resultados):
    respostas_certas = 0
    for questao, (escolha, correta) in resultados.items():
        if escolha == correta:
            st.toast(f':green-background[{questao}: Resposta Certa!]', icon='🎉')
            respostas_certas += 1
        else:
            st.toast(f':red-background[{questao}: Resposta Errada. Correto: {correta}]', icon="⚠️")
        time.sleep(1)  # Pequeno delay para evitar que os toasts apareçam todos de uma vez

    # Reseta o estado para nova rodada
    st.session_state["respondidas"] = set()
    st.session_state["embaralho"] = np.random.permutation(["Alternativa_A", "Alternativa_B", "Alternativa_C", "Alternativa_D", "Alternativa_E"])
    st.write(f"Você acertou {respostas_certas} de {len(resultados)} questões!")

local_css(r"styles_questao.css")

    
