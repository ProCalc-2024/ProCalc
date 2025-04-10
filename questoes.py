import streamlit as st
import pandas as pd
import gspread
from streamlit_gsheets import GSheetsConnection
import numpy as np
import time
import random
import requests
import base64

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css(r"styles_questao.css")

def read_questao():
    GITHUB_TOKEN = st.secrets["github"]["token"]
    REPO_OWNER = st.secrets["github"]["repo_owner"]
    REPO_NAME = st.secrets["github"]["repo_name"]
    BRANCH = st.secrets["github"]["branch"]

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

    lista = list(set(dict["Materia"]))lista = list(set(dict["Materia"]))
    lista.sort()
    lista.insert(0, "Todas")  # Adiciona a opção "Todas" no topo

    with col1:
        materia = st.selectbox("Selecione um assunto", lista, disabled=disabled3)

    if materia == "Todas":
        lista_ques = [linha for linha in dict.iloc]
    else:
        lista_ques = [linha for linha in dict.iloc if linha["Materia"] == materia]
    n = len(lista_ques)

    with col1:
        numero = st.number_input("Quantas questões você gostaria de fazer?", min_value=1, max_value=n, value=1, disabled=disabled3)

    tab_names = [f"Q{i}" for i in range(numero + 1)]
    tab_names[0] = "Informações"
    tab_names.append("Resposta")
    tabs = st.tabs(tab_names)

    col_list = [1] * numero
    coluna = st.columns(col_list)

    with col1:
        st.title("Perguntas")

    with tabs[0]:
        st.info('This is a purely informational message', icon="ℹ️")

    botao = st.session_state["botao"]

    # Verificação de inicialização
    if "ques" not in st.session_state or st.session_state.get("materia_atual") != materia:
        st.session_state["save"] = {}
        st.session_state["numero"] = 0
        st.session_state["ques"] = list(range(len(lista_ques)))
        random.shuffle(st.session_state["ques"])
        st.session_state["materia_atual"] = materia
        st.rerun()

    b1 = st.session_state["ques"]

    for i in range(numero):
        j = i + 1
        with tabs[j]:
            disabled2 = st.session_state["disabled"]
            lista_alt = ["Alternativa_A", "Alternativa_B", "Alternativa_C", "Alternativa_D", "Alternativa_E"]

            if f"embaralho{i}{materia}" not in st.session_state:
                st.session_state[f"embaralho{i}{materia}"] = np.random.choice(lista_alt, 5, replace=False)

            questao_index = b1[i]
            evitar.append(questao_index)

            embaralho = st.session_state[f"embaralho{i}{materia}"]
            questao = lista_ques[questao_index]

            st.write(questao["Enunciado"])

            file_name = questao["Imagem"]
            if pd.notna(file_name) and file_name != "":
                with st.expander("Visualizar imagem"):
                    file_path = f"imagens/{file_name}"
                    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file_path}"
                    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
                    response = requests.get(url, headers=headers)

                    if response.status_code == 200:
                        file_data = response.json()
                        image_base64 = file_data["content"]
                        image_data = base64.b64decode(image_base64)
                        st.image(image_data, caption="", use_column_width=True)
                    else:
                        st.error(f"Erro ao buscar a imagem: {response.json()}")

            st.subheader('', divider='gray')

            opcoes[i] = [questao[embaralho[j]] for j in range(5)]
            alternativa[i] = st.radio("", options=opcoes[i], index=None, key=f"key{i}", disabled=disabled2)

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
                    if resposta[i]:
                        st.success(f'A resposta correta é {questao["Alternativa_A"]}', icon="✅")
                    else:
                        st.error(f'A resposta correta é {questao["Alternativa_A"]}', icon="🚨")

    with tabs[numero + 1]:
        if botao:
            acertos = sum(resposta[i] for i in resposta)
            porcen = (acertos / numero)
            progress_text = f"{round(porcen * 100, 1)}% de acertos"
            st.progress(porcen, text=progress_text)

            if porcen < 0.6:
                st.toast(f':red-background[Você Acertou {round(porcen * 100, 1)}%]', icon="⚠️")
            else:
                st.toast(f':green-background[Você Acertou {round(porcen * 100, 1)}%]', icon='🎉')

    for i in range(numero):
        y = i + 1
        with tabs[numero + 1]:
            if botao and alternativa[i] is None:
                st.radio(tab_names[y], options=opcoes[i], index=None, key=f"cha4{y}", disabled=True, horizontal=True)
                st.warning('Nenhuma das alternativas foi selecionada.', icon="⚠️")
                res[i] = False
            else:
                if not botao:
                    if alternativa[i] is not None:
                        index2 = opcoes[i].index(alternativa[i])
                        st.radio(tab_names[y], options=opcoes[i], index=index2, key=f"cha1{y}", disabled=True, horizontal=True)
                    else:
                        st.radio(tab_names[y], options=opcoes[i], index=None, key=f"cha2{y}", disabled=True, horizontal=True)

                if botao and alternativa[i] is not None:
                    index2 = opcoes[i].index(alternativa[i])
                    st.radio(tab_names[y], options=opcoes[i], index=index2, key=f"cha3{y}", disabled=True, horizontal=True)
                    if resposta[i]:
                        st.success(f'A resposta correta é {questao["Alternativa_A"]}', icon="✅")
                    else:
                        st.error(f'A resposta correta é {questao["Alternativa_A"]}', icon="🚨")
                    res[i] = True

    with tabs[numero + 1]:
        def clicar_botao22():
            st.session_state["disabledtime"] = False

        def clicar_botao():
            st.session_state["botao"] = True
            st.session_state["disabled"] = True

        def new_questionario():
            start_timer()
            st.session_state["botao"] = None
            st.session_state["disabled"] = False
            st.session_state["disabledtime"] = True
            st.session_state["ques"] = list(range(len(lista_ques)))
            random.shuffle(st.session_state["ques"])
            for i in range(n):
                st.session_state[f"embaralho{i}{materia}"] = np.random.choice(lista_alt, 5, replace=False)

        if not st.session_state["botao"]:
            if st.button("Submeter", on_click=clicar_botao):
                pass

        if st.session_state["botao"]:
            if st.button("Novas Perguntas", on_click=clicar_botao22):
                pass

    with col2:
        min_question = st.slider("Tempo de resolução do formulario minutos:", 0, 59, 0, disabled=disabled3)
        hor_question = st.slider("Tempo de resolução do formulario horas:", 0, 6, 0, disabled=disabled3)
        total_time = hor_question * 60 * 60 + min_question * 60

        if not disabled3:
            st.write(f"⏳ {hor_question:02}:{min_question:02}:00")

        if "time_left" not in st.session_state:
            st.session_state.time_left = total_time
        if "start_time" not in st.session_state:
            st.session_state.start_time = None
        if "running" not in st.session_state:
            st.session_state.running = False

        def start_timer():
            st.session_state.running = True
            st.session_state.start_time = time.time()

        def update_timer():
            if st.session_state.running:
                elapsed_time = int(time.time() - st.session_state.start_time)
                st.session_state.time_left = max(0, total_time - elapsed_time)

                if st.session_state["botao"]:
                    st.session_state.time_left = 0

                if st.session_state.time_left == 0:
                    st.session_state.running = False
                    clicar_botao()

        if st.session_state.running:
            update_timer()
            hours, remainder = divmod(st.session_state.time_left, 3600)
            minutes, seconds = divmod(remainder, 60)
            formatted_time = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
            st.write(f"⏳ {formatted_time}")
            time.sleep(1)
            st.rerun()
        elif st.session_state.time_left == 0 and disabled3:
            st.write("⏳ Tempo finalizado")

        if st.session_state["disabled"] in [True, False]:
            if st.button("Iniciar questionario", on_click=new_questionario):
                pass

        

