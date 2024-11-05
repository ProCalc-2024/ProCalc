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

    enunciado = st.text_area("Enunciado", placeholder= "digite aqui o enunciado da questão", key = "enunciado")
    letra_a = st.text_input("Resposta1", placeholder= "digite aqui a resposta correta", key = "letra_a") 
    letra_b = st.text_input("Resposta2", placeholder= "digite aqui a resposta2", key = "letra_b")
    letra_c = st.text_input("Resposta3", placeholder= "digite aqui a resposta3", key = "letra_c") 
    letra_d = st.text_input("Resposta4", placeholder= "digite aqui a resposta4", key = "letra_d") 
    letra_e = st.text_input("Resposta5", placeholder= "digite aqui a resposta5", key = "letra_e")

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
        
        st.success(':green-background[Questão salva]', icon='✔️')
        
        st.rerun()

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
        questao_selecionada = st.selectbox("Selecione a questão a editar", options=questoes_list)

    
    questao_atual = questoes_filtradas[questoes_filtradas["Enunciado"] == questao_selecionada].iloc[0]

    
    descricao = st.text_input("Descrição", value=questao_atual["Descrição"])
    enunciado = st.text_area("Enunciado", value=questao_atual["Enunciado"])
    letra_a = st.text_input("Resposta1", value=questao_atual["Alternativa_A"])
    letra_b = st.text_input("Resposta2", value=questao_atual["Alternativa_B"])
    letra_c = st.text_input("Resposta3", value=questao_atual["Alternativa_C"])
    letra_d = st.text_input("Resposta4", value=questao_atual["Alternativa_D"])
    letra_e = st.text_input("Resposta5", value=questao_atual["Alternativa_E"])

    
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
    
    # Verifica as colunas do DataFrame
    st.write("Colunas disponíveis no DataFrame:", dict.columns.tolist())

    # Colunas para seleção de matéria e questão
    col1, col2 = st.columns([1, 2])

    # Seleção de matéria
    with col1:
        materias_unicas = dict["Materia"].unique()
        materia_selecionada = st.selectbox("Selecione a Matéria:", options=materias_unicas)

    # Filtra as questões pela matéria selecionada
    questoes_filtradas = dict[dict["Materia"] == materia_selecionada]

    # Verifica se a coluna 'Enunciado' existe no DataFrame filtrado
    if "Enunciado" not in questoes_filtradas.columns:
        st.error("A coluna 'Enunciado' não foi encontrada. Verifique o nome da coluna no Google Sheets.")
        return

    # Seleção de questão a ser deletada
    with col2:
        questoes_dict = {f"{i + 1}. {row['Materia']} - {row['Enunciado'][:50]}": index for i, (index, row) in enumerate(questoes_filtradas.iterrows())}
        questao_selecionada = st.selectbox("Questões:", options=list(questoes_dict.keys()))

    # Botão para confirmar exclusão
    if st.button("Deletar Questão"):
        index_questao = questoes_dict[questao_selecionada]
        dict = dict.drop(index_questao).reset_index(drop=True)
        
        # Atualiza a planilha com o dataframe sem a questão excluída
        conn.update(worksheet="Questões", data=dict)
        
        # Atualiza cache para refletir a exclusão
        conn.read(worksheet="Questões", ttl="1s")
        
        st.toast(':green-background[Questão deletada com sucesso]', icon='✔️')
        time.sleep(2)
        st.experimental_rerun()

