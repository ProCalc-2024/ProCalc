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

    col1, col2 = st.columns([1, 1])
    test = {}
    resul = {}
    b = []
    evitar = []
    resposta = {}
    alternativa = {}
    res = {}
    opcoes = {}
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
    with col2: 
        # Pergunta ao usuário quantas questões deseja criar
        numero = st.number_input("Quantas questões você gostaria de fazer?", min_value=1, max_value=n, value=1)
        
    tab_names = []
    # Cria uma lista de nomes para as questões
    tab_names = [f"Q{i}" for i in range(numero + 1)]
    tab_names[0] = "Informações"
    tab_names.append("Resposta")
    # Cria as abas dinamicamente
    tabs = st.tabs(tab_names)
    
    time_per_question = 60
    # Inicializar variáveis de sessão
    if "current_question" not in st.session_state:
        st.session_state.current_question = 1
    if "time_left" not in st.session_state:
        st.session_state.time_left = time_per_question
    if "start_time" not in st.session_state:
        st.session_state.start_time = None
    if "running" not in st.session_state:
        st.session_state.running = False
    
    # Função para iniciar o temporizador
    def start_timer():
        st.session_state.running = True
        st.session_state.start_time = time.time()
    
    # Função para atualizar o temporizador
    def update_timer():
        if st.session_state.running:
            elapsed_time = int(time.time() - st.session_state.start_time)
            st.session_state.time_left = max(0, time_per_question - elapsed_time)
    
            # Verificar se o tempo da questão acabou
            if st.session_state.time_left == 0:
                if st.session_state.current_question < numero:
                    st.session_state.current_question += 1
                    st.session_state.time_left = time_per_question
                    st.session_state.start_time = time.time()  # Reiniciar o tempo
                else:
                    st.session_state.running = False  # Parar o temporizador
    
    # Interface do Temporizador
    if st.session_state.running:
        update_timer()
        st.write(f"**Question {st.session_state.current_question}**")
        st.write(f"Time left: {st.session_state.time_left} seconds")
        time.sleep(1)  # Atualizar a cada 1 segundo
        st.experimental_rerun()
    elif st.session_state.current_question > numero:
        st.write("🎉 All questions completed!")
    start_timer()    
    
    #with tabs[numero]:
    col_list = [1] * numero
    coluna = st.columns(col_list)
    with col1:
        st.title("Perguntas")
    with tabs[0]:
        st.info('This is a purely informational message', icon="ℹ️")
        
    botao = st.session_state["botao"]
        
    for i in range(numero):
        j=i+1
        
        with tabs[i+1]:
            
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
            b1 = st.session_state["ques"]
            
            # Verifique se há opções válidas disponíveis
            if opcoes_validas:
                numero_aleatorio = np.random.choice(opcoes_validas)
           
            evitar.append(b1[i])
            
            embaralho = st.session_state[f"embaralho{i}{materia}"]
            # Escolha de questão aleatória
            questao = lista_ques[b1[i]]
            
            st.write(questao["Enunciado"])
            st.subheader('', divider='gray')
            
            # Exibe as alternativas embaralhadas
            opcoes[i] = [questao[embaralho[j]] for j in range(5)]
            
            alternativa[i] = st.radio("", options=opcoes[i], index=None, key = f"key{i}", disabled=disabled2)
            
            st.session_state["resposta"] = questao["Alternativa_A"]
            resul.update(st.session_state["save"])                                                
            st.session_state["save"] = {st.session_state["numero"] + 1: st.session_state["ques"]}
            sequencia = st.session_state["save"]
            resul.update(sequencia)
            st.session_state["save"] = resul
            resposta[i] = alternativa[i] == questao["Alternativa_A"]

            if botao and alternativa[i] is None:
                st.warning('Nenhuma das alternativas foi selecionada.', icon="⚠️")
            else:
                
                if botao and alternativa[i] is not None:
                    
                    if resposta[i] == True:
                                
                        st.success(f'A resposta correta e {questao["Alternativa_A"]}', icon="✅")
                 
                    if resposta[i] == False:  
                
                        st.error(f'A resposta correta e {questao["Alternativa_A"]}', icon="🚨")
    
    with tabs[numero+1]:
        if botao:
            acertos = 0
            for i in resposta:  
                if resposta[i] == True:
                    acertos = acertos + 1
                    
            porcen = (acertos/numero)
            progress_text = f"{round(porcen*100, 1)}% de acertos"
            st.progress(porcen, text=progress_text)
            if porcen < 0.6:
                st.toast(f':red-background[Você Acertou {round(porcen*100, 1)}%]', icon="⚠️")
            else:
                st.toast(f':green-background[Você Acertou {round(porcen*100, 1)}%]', icon='🎉')
            
        
        
    for i in range(numero):    
        y=i+1
        with tabs[numero+1]:
             
            if botao and alternativa[i] is None:
                st.radio(tab_names[y], options=opcoes[i], index=None, key=f"cha4{y}", disabled=True, horizontal=True)
                st.warning('Nenhuma das alternativas foi selecionada.', icon="⚠️")
                res[i] = False
            else:
                if botao is not True:
                    x=0
                    if alternativa[i] is not None:
                        index2 = opcoes[i].index(alternativa[i])
                        st.radio(tab_names[y], options=opcoes[i], index=index2, key=f"cha1{y}", disabled=True, horizontal=True) 
                        x = 1
                        
                    if x == 0:  
                        st.radio(tab_names[y], options=opcoes[i], index=None, key=f"cha2{y}", disabled=True, horizontal=True)
                        
                if botao and alternativa[i] is not None:
                    
                    index2 = opcoes[i].index(alternativa[i])
                    st.radio(tab_names[y], options=opcoes[i], index=index2, key=f"cha3{y}", disabled=True, horizontal=True) 
                    
                    if resposta[i] == True:
                                
                        st.success(f'A resposta correta e {questao["Alternativa_A"]}', icon="✅")
                 
                    if resposta[i] == False:  
                
                        st.error(f'A resposta correta e {questao["Alternativa_A"]}', icon="🚨")
                    res[i] = True
    
    with tabs[numero+1]:   
        def clicar_botao():
            st.session_state["botao"] = True
            st.session_state["disabled"] = True
            

        def new_questionario():
            st.session_state["botao"] = None
            st.session_state["disabled"] = False
            random.shuffle(b)
            st.session_state["ques"] = b
            for i in range(n):
                st.session_state[f"embaralho{i}{materia}"] = np.random.choice(lista, 5, replace=False)
            
            
        # Mostra o botão somente se ele ainda não foi clicado
        if not st.session_state["botao"]:
            if st.button("Submeter",on_click=clicar_botao):
                pass  # O estado muda ao clicar, e o botão desaparece na próxima renderização

        if st.session_state["botao"]:       
            if st.button("Novas Perguntas", on_click=new_questionario):
                pass  # O estado muda ao clicar, e o botão desaparece na próxima renderização
        
        # Define a variável com base no estado do botão
        botao = st.session_state["botao"]
