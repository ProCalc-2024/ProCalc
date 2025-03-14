import streamlit as st
import pandas as pd
import gspread
from streamlit_gsheets import GSheetsConnection
import numpy as np
import requests
import base64

def inserir_ques():   
    # Carregar configurações do secrets para o github
    GITHUB_TOKEN = st.secrets["github"]["token"]
    REPO_OWNER = st.secrets["github"]["repo_owner"]
    REPO_NAME = st.secrets["github"]["repo_name"]
    BRANCH = st.secrets["github"]["branch"]
    
    # Upload da imagem pelo usuário
    uploaded_file = st.file_uploader("Insira uma imagem:", type=["jpg", "png", "jpeg"])
        
    conn = st.connection("gsheets", type=GSheetsConnection)
    sheet = conn.read(worksheet="Materias")
    dict = pd.DataFrame(sheet)
    # adicionar uma nova pergunta
    result = {}
    
    col1, col2 = st.columns([1, 1])

    lista =  [linha for linha in dict["Materia"]]

    with col2:
        materia = st.selectbox("Selecione uma matéria:", lista)

    with col1:
        descricao = st.text_input("Descrição:")

    enunciado = st.text_area("Enunciado", placeholder= "Digite aqui o enunciado da questão", key = "enunciado")
    letra_a = st.text_input("Resposta 1", placeholder= "Digite aqui a resposta correta", key = "letra_a") 
    letra_b = st.text_input("Resposta 2", placeholder= "Digite aqui a resposta 2", key = "letra_b")
    letra_c = st.text_input("Resposta 3", placeholder= "Digite aqui a resposta 3", key = "letra_c") 
    letra_d = st.text_input("Resposta 4", placeholder= "Digite aqui a resposta 4", key = "letra_d") 
    letra_e = st.text_input("Resposta 5", placeholder= "Digite aqui a resposta 5", key = "letra_e")

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
      
    lista_ques = []
    with st.expander("Visualizar questão"):
        
        st.subheader('', divider = 'gray')
    
        # embaralha as alternativas independente da questão 
        lista = ["Alternativa_A","Alternativa_B","Alternativa_C","Alternativa_D","Alternativa_E"]
        
        if "embaralho" not in st.session_state:
            
            st.session_state["embaralho"] = np.random.choice(lista, 5, replace = False)
    
        if "ques" not in st.session_state:
            st.session_state["save"] = {}
            st.session_state["numero"] = 0
             
        embaralho = st.session_state["embaralho"]
        
        # escolha de questão aleatoria
        for linha in novo.iloc: 
            lista_ques.append(linha)
    
        #comando da questão  
        questao = lista_ques[0]
        
        st.write("")
        st.write(questao["Enunciado"])

        st.subheader('', divider = 'gray')
        
        opções = [questao[embaralho[0]], questao[embaralho[1]], questao[embaralho[2]], questao[embaralho[3]], questao[embaralho[4]]]    
        
        alternativa = st.radio("", options = opções, index=None)
            
        st.session_state["resposta"] = questao["Alternativa_A"]

    if st.button("Salvar"):

        if uploaded_file is not None:
            
            image_data = uploaded_file.getvalue()  # Lê os bytes da imagem
            image_base64 = base64.b64encode(image_data).decode()  # Converte para Base64
                
            file_path = f"imagens/{uploaded_file.name}"  # Caminho no repositório
                
            novo['Imagem'] = [f"{uploaded_file.name}"]
                
            url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file_path}"
                
            payload = {
                "message": f"Adicionando {uploaded_file.name} via Streamlit",
                "content": image_base64,
                "branch": BRANCH
            }
            
            headers = {"Authorization": f"token {GITHUB_TOKEN}"}
            
            response = requests.put(url, json=payload, headers=headers)
            
            if response.status_code == 201:
                combined_data = pd.concat([existing_data, novo], ignore_index=True)
                conn.update(worksheet="Questões", data=combined_data)
           
                conn.read(
                worksheet="Questões",  # Nome da planilha
                ttl="10m"                  # Cache de 1 segundo
                )
                
                st.success(':green-background[Questão salva]', icon='✔️')
            
                st.rerun()
                
                st.success(f"Imagem Salva no GITHUB! 📤")
            else:
                #st.error(f"Erro ao enviar a imagem: {response.json()}")
                st.error(f"A imagem já existe")
        
        
        else:
            combined_data = pd.concat([existing_data, novo], ignore_index=True)
            
            conn.update(worksheet="Questões", data=combined_data)
           
            conn.read(
            worksheet="Questões",  # Nome da planilha
            ttl="1s"                  # Cache de 1 segundo
            )
            
            st.success(':green-background[Questão salva]', icon='✔️')
        
            st.rerun()

def inserir_assun():    
    
    conn = st.connection("gsheets", type=GSheetsConnection)
    existing = conn.read(worksheet="Materias")
    # adicionar uma nova pergunta
    result = {}

    st.title("Novo Assunto")
    
    assun = st.text_area("Assunto:", placeholder= "Digite aqui o novo assunto") 
    
    new = pd.DataFrame({
        'Materia': [assun]
     })
    
    combined = pd.concat([existing, new], ignore_index=True) 
    
    if st.button("Visualizar questão"):
        
        conn.update(worksheet="Materias", data=combined)
       
        conn.read(
        worksheet="Materias",  # Nome da planilha
        ttl="10m"                  # Cache de 10 minutos
        )
        
              
def editar_ques():
    conn = st.connection("gsheets", type=GSheetsConnection)
    existing_data = conn.read(worksheet="Questões")
    
    if existing_data.empty:
        st.warning("Nenhuma questão disponível para editar.")
        return
    
    
    materias_unicas = existing_data["Materia"].unique()
    
    
    col1, col2 = st.columns(2)

    with col1:
        materia = st.selectbox("Matéria", options=materias_unicas)

    with col2:
        
        questoes_filtradas = existing_data[existing_data["Materia"] == materia]
        
        
        if questoes_filtradas.empty:
            st.warning(f"Nenhuma questão disponível para a matéria '{materia}'.")
            return

        questoes_list = questoes_filtradas["Enunciado"].tolist()
        questao_selecionada = st.selectbox("Selecione a questão a editar:", options=questoes_list)

    
    questao_atual = questoes_filtradas[questoes_filtradas["Enunciado"] == questao_selecionada].iloc[0]

    
    descricao = st.text_input("Descrição", value=questao_atual["Descrição"])
    enunciado = st.text_area("Enunciado", value=questao_atual["Enunciado"])
    letra_a = st.text_input("Resposta 1", value=questao_atual["Alternativa_A"])
    letra_b = st.text_input("Resposta 2", value=questao_atual["Alternativa_B"])
    letra_c = st.text_input("Resposta 3", value=questao_atual["Alternativa_C"])
    letra_d = st.text_input("Resposta 4", value=questao_atual["Alternativa_D"])
    letra_e = st.text_input("Resposta 5", value=questao_atual["Alternativa_E"])

    
    if st.button("Salvar"):
        
        existing_data.loc[existing_data["Enunciado"] == questao_selecionada, ["Materia", "Descrição", "Enunciado", "Alternativa_A", "Alternativa_B", "Alternativa_C", "Alternativa_D", "Alternativa_E"]] = [
            materia, descricao, enunciado, letra_a, letra_b, letra_c, letra_d, letra_e
        ]
        
        conn.update(worksheet="Questões", data=existing_data)
        st.success("Questão editada com sucesso!")


def deletar_ques():
    # Conexão com o Google Sheets
    conn = st.connection("gsheets", type=GSheetsConnection)
    sheet = conn.read(worksheet="Questões")
    dict = pd.DataFrame(sheet)

    st.title("Deletar Questão")

    # Colunas para seleção de matéria e questão
    col1, col2 = st.columns([1, 2])

    # Seleção de matéria
    with col1:
        materias_unicas = dict["Materia"].unique()
        materia_selecionada = st.selectbox("Selecione a Matéria:", options=materias_unicas)

    # Filtra as questões pela matéria selecionada
    questoes_filtradas = dict[dict["Materia"] == materia_selecionada]

    # Seleção de questão a ser deletada, tratando possíveis NaNs em 'Enunciado'
    with col2:
        questoes_dict = {
            f"{i + 1}. {row['Materia']} - {str(row['Enunciado'])[:50]}" if pd.notnull(row['Enunciado']) else f"{i + 1}. {row['Materia']} - [Sem enunciado]": index
            for i, (index, row) in enumerate(questoes_filtradas.iterrows())
        }
        questao_selecionada = st.selectbox("Questões:", options=list(questoes_dict.keys()))

    # Exibe as informações da questão selecionada
    index_questao = questoes_dict[questao_selecionada]
    questao_info = dict.loc[index_questao]
    st.write("Informações da questão selecionada para exclusão:")
    st.write(questao_info)

    # Botão para confirmar exclusão
    if st.button("Deletar Questão"):
        dict = dict.drop(index_questao).reset_index(drop=True)

        # Atualiza a planilha com o dataframe sem a questão excluída
        conn.update(worksheet="Questões", data=dict)

        # Atualiza cache para refletir a exclusão
        conn.read(worksheet="Questões", ttl="1s")

        st.toast(':green-background[Questão deletada com sucesso]', icon='✔️')
        st.rerun()
