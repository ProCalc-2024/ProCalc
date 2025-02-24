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
        st.session_state["disabled"] = True
        st.session_state["disabledtime"] = False
    
    disabled3 = st.session_state["disabledtime"]
    
    # lista de matérias
    lista = list(set(dict["Materia"]))
    
    with col1:       
        materia = st.selectbox("Selecione um assunto", lista,disabled=disabled3)    

    # lista de questões de acordo com a matéria escolhida
    lista_ques = [linha for linha in dict.iloc if linha["Materia"] == materia]

    # Número de questões
    n = len(lista_ques)
    with col1: 
        # Pergunta ao usuário quantas questões deseja criar
        numero = st.number_input("Quantas questões você gostaria de fazer?", min_value=1, max_value=n, value=1, disabled=disabled3)
        
    tab_names = []
    # Cria uma lista de nomes para as questões
    tab_names = [f"Q{i}" for i in range(numero + 1)]
    tab_names[0] = "Informações"
    tab_names.append("Resposta")
    # Cria as abas dinamicamente
    tabs = st.tabs(tab_names)   
    
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
                st.rerun()
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
            st.write(questao["Imagem"])
            with st.expander("Visualizar Imagem"):
                # Nome do arquivo (você pode definir dinamicamente)
                file_name = ""
                
                if file_name:
                    file_path = f"imagens/{file_name}"
                    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file_path}"
                
                    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
                    response = requests.get(url, headers=headers)
                
                    if response.status_code == 200:
                        file_data = response.json()
                        image_base64 = file_data["content"]  # Pega o conteúdo Base64
                        image_data = base64.b64decode(image_base64)  # Decodifica de Base64 para bytes
                
                        # Exibir a imagem no Streamlit
                        st.image(image_data, caption=file_name, use_column_width=True)
                    else:
                        st.error(f"Erro ao buscar a imagem: {response.json()}")
            
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
        def clicar_botao22():
            st.session_state["disabledtime"]  = False
            
        def clicar_botao():
            st.session_state["botao"] = True
            st.session_state["disabled"] = True
            
        def new_questionario():
            start_timer()
            st.session_state["botao"] = None
            st.session_state["disabled"] = False
            st.session_state["disabledtime"]  = True
            random.shuffle(b)
            st.session_state["ques"] = b
            for i in range(n):
                st.session_state[f"embaralho{i}{materia}"] = np.random.choice(lista, 5, replace=False)    
            
        # Mostra o botão somente se ele ainda não foi clicado
        if not st.session_state["botao"]:
            
            if st.button("Submeter",on_click=clicar_botao):
                pass  # O estado muda ao clicar, e o botão desaparece na próxima renderização
        
        if st.session_state["botao"]:       
            
            if st.button("Novas Perguntas", on_click=clicar_botao22):
                pass  # O estado muda ao clicar, e o botão desaparece na próxima renderização
        
        # Define a variável com base no estado do botão
        botao = st.session_state["botao"]
    
    with col2:

                
        min_question = st.slider("tempo de resolução do formulario minutos", 0, 59, 0,  disabled=disabled3)        
        hor_question = st.slider("tempo de resolução do formulario horas", 0, 6, 0, disabled=disabled3)
        
        # Calcular o tempo total
        total_time = hor_question*60*60 + min_question*60
        
        if not disabled3:
            st.write(f"⏳ {hor_question:02}:{min_question:02}:00")
        
        # Inicializar variáveis de sessão
        if "time_left" not in st.session_state:
            st.session_state.time_left = total_time
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
                st.session_state.time_left = max(0, total_time - elapsed_time)

                if st.session_state["botao"] == True:
                    st.session_state.time_left = 0
                
                # Verificar se o tempo total acabou
                if st.session_state.time_left == 0:
                    st.session_state.running = False
                    clicar_botao()
            
        # Interface do Temporizador
        if st.session_state.running:
            
            update_timer()
            # Converter segundos para horas, minutos e segundos
            hours, remainder = divmod(st.session_state.time_left, 3600)
            minutes, seconds = divmod(remainder, 60)
            formatted_time = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
            # Exibir o tempo restante
            st.write(f"⏳ {formatted_time}")

            time.sleep(1)  # Atualizar a cada 1 segundo
            st.rerun()
        
        elif st.session_state.time_left == 0:
            if disabled3:
                st.write("⏳ Tempo finalizado")
        
        if st.session_state["disabled"] == True or st.session_state["disabled"] == False:
            if st.button("Iniciar questionario", on_click=new_questionario):
                pass
        #iniciar o temporizador
        
        

