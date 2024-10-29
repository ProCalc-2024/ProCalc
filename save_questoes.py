import streamlit as st
import pandas as pd
import gspread
from streamlit_gsheets import GSheetsConnection
import numpy as np
def inserir_ques():    
    
    conn = st.connection("gsheets", type=GSheetsConnection)
    sheet = conn.read(worksheet="Materias")
    dict = pd.DataFrame(sheet)
    # adicionar uma nova pergunta
    result = {}
    
    col1, col2 = st.columns([1, 1])

    lista =  [linha for linha in dict["Materia"]]

    with col2:
        materia = st.selectbox("selecione uma materia", lista)

    with col1:
        descricao = st.text_input("descrição")

    enunciado = st.text_area("Enunciado", placeholder= "digite aqui o enunciado da questão")
    letra_a = st.text_input("Resposta1", placeholder= "digite aqui a resposta correta") 
    letra_b = st.text_input("Resposta2", placeholder= "digite aqui a resposta2")
    letra_c = st.text_input("Resposta3", placeholder= "digite aqui a resposta3") 
    letra_d = st.text_input("Resposta4", placeholder= "digite aqui a resposta4") 
    letra_e = st.text_input("Resposta5", placeholder= "digite aqui a resposta5")

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
    
    combined_data = pd.concat([existing_data, novo], ignore_index=True)
    lista_ques = []
    with st.expander("Visualizar Questão"):
        
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
    
        butao = st.button("Submeter") 
                
        # salva a sequencia de questoes

        resposta = alternativa == questao["Alternativa_A"]
        
        if butao and resposta:         
            st.toast(':green-background[Resposta Certa]', icon='🎉')
            time.sleep(5)
            st.rerun()
    
        elif butao and (resposta is False):
            st.toast(':red-background[Resposta Errada]', icon="⚠️")
            time.sleep(5)
        
    if st.button("Salvar"):   
        
            
        conn.update(worksheet="Questões", data=combined_data)
       
        conn.read(
        worksheet="Questões",  # Nome da planilha
        ttl="10m"                  # Cache de 10 minutos
        )
        st.toast(':green-background[Questão salva]', icon='✔️')
        time.sleep(2)
        st.experimental_rerun()
        
        

def inserir_assun():    
    
    conn = st.connection("gsheets", type=GSheetsConnection)
    existing = conn.read(worksheet="Materias")
    # adicionar uma nova pergunta
    result = {}

    st.title("Novo Assunto")
    
    assun = st.text_area("assunto", placeholder= "digite aqui o enunciado da questão") 
    
    new = pd.DataFrame({
        'Materia': [assun]
     })
    
    combined = pd.concat([existing, new], ignore_index=True) 
    
    if st.button("visualizar questão"):
        
        conn.update(worksheet="Materias", data=combined)
       
        conn.read(
        worksheet="Materias",  # Nome da planilha
        ttl="10m"                  # Cache de 10 minutos
        )
        
              
# Função para Editar Questões
def editar_ques():
    conn = st.connection("gsheets", type=GSheetsConnection)
    existing_data = conn.read(worksheet="Questões")
    
    if existing_data.empty:
        st.warning("Nenhuma questão disponível para editar.")
        return
    
    # Lista de questões para edição
    questoes_list = existing_data["Enunciado"].tolist()
    questao_selecionada = st.selectbox("Selecione a questão a editar", options=questoes_list)

    # Obter dados da questão selecionada
    questao_atual = existing_data[existing_data["Enunciado"] == questao_selecionada].iloc[0]

    # Materias disponíveis
    materias_unicas = existing_data["Materia"].unique()
    
    # Define o índice inicial baseado na matéria atual
    index_inicial = list(materias_unicas).index(questao_atual["Materia"]) if questao_atual["Materia"] in materias_unicas else 0

    # Selecionar matéria
    materia = st.selectbox("Matéria", options=materias_unicas, index=index_inicial)

    # Campos para edição
    descricao = st.text_input("Descrição", value=questao_atual["Descrição"])
    enunciado = st.text_area("Enunciado", value=questao_atual["Enunciado"])
    letra_a = st.text_input("Resposta1", value=questao_atual["Alternativa_A"])
    letra_b = st.text_input("Resposta2", value=questao_atual["Alternativa_B"])
    letra_c = st.text_input("Resposta3", value=questao_atual["Alternativa_C"])
    letra_d = st.text_input("Resposta4", value=questao_atual["Alternativa_D"])
    letra_e = st.text_input("Resposta5", value=questao_atual["Alternativa_E"])

    # Botão para salvar alterações
    if st.button("Salvar"):
        # Atualiza os dados da questão
        existing_data.loc[existing_data["Enunciado"] == questao_selecionada, ["Materia", "Descrição", "Enunciado", "Alternativa_A", "Alternativa_B", "Alternativa_C", "Alternativa_D", "Alternativa_E"]] = [
            materia, descricao, enunciado, letra_a, letra_b, letra_c, letra_d, letra_e
        ]
        
        conn.update(worksheet="Questões", data=existing_data)
        st.success("Questão editada com sucesso!")
