import streamlit as st
import pandas as pd
import gspread
from streamlit_gsheets import GSheetsConnection
import numpy as np
import requests
import base64

def inserir_video():
    # 1. Configurações de acesso (GitHub)
    GITHUB_TOKEN = st.secrets["github"]["token"]
    REPO_OWNER = st.secrets["github"]["repo_owner"]
    REPO_NAME = st.secrets["github"]["repo_name"]
    BRANCH = st.secrets["github"]["branch"]

    st.header("📹 Adicionar Novo Vídeo")

    # 2. Conexão com Google Sheets
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Carregar matérias para o selectbox
    df_materias = conn.read(worksheet="Materias")
    lista_materias = df_materias["Materia"].tolist()

    # 3. Interface de Usuário (Inputs)
    col1, col2 = st.columns(2)
    with col1:
        materia = st.selectbox("Selecione a matéria:", lista_materias, key="video_materia")
    with col2:
        titulo = st.text_input("Título do Vídeo:", placeholder="Ex: Aula 01 - Introdução")

    descricao = st.text_area("Descrição/Resumo:", placeholder="Sobre o que é este vídeo?")
    
    # Opção de Upload ou Link Externo (YouTube/Drive)
    tipo_input = st.radio("Origem do vídeo:", ["Upload de Arquivo", "Link Externo (YouTube/URL)"], horizontal=True)

    video_url_final = ""
    uploaded_video = None

    if tipo_input == "Upload de Arquivo":
        uploaded_video = st.file_uploader("Selecione o vídeo (mp4, mov, avi):", type=["mp4", "mov", "avi"])
    else:
        video_url_final = st.text_input("Cole a URL do vídeo:")

    # 4. Lógica de Salvamento
    if st.button("Salvar Vídeo"):
        # Lógica de Upload para GitHub (se houver arquivo)
        if uploaded_video is not None:
            video_bytes = uploaded_video.getvalue()
            video_base64 = base64.b64encode(video_bytes).decode()
            file_path = f"videos/{uploaded_video.name}"
            
            url_github = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file_path}"
            payload = {
                "message": f"Adicionando vídeo {uploaded_video.name} via Streamlit",
                "content": video_base64,
                "branch": BRANCH
            }
            headers = {"Authorization": f"token {GITHUB_TOKEN}"}
            
            with st.spinner("Enviando vídeo para o GitHub..."):
                response = requests.put(url_github, json=payload, headers=headers)
            
            if response.status_code in [201, 200]:
                # Se for upload, salvamos o caminho do arquivo ou a URL bruta do GitHub
                video_url_final = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}/{file_path}"
                st.toast("Vídeo enviado ao GitHub com sucesso!", icon="📤")
            else:
                st.error("Erro ao enviar para o GitHub. Verifique o tamanho do arquivo.")
                return

        # Salvar no Google Sheets
        if video_url_final or uploaded_video:
            existing_data = conn.read(worksheet="Videos")
            
            novo_video = pd.DataFrame({
                'Materia': [materia],
                'Titulo': [titulo],
                'Descrição': [descricao],
                'URL_Video': [video_url_final]
            })

            combined_data = pd.concat([existing_data, novo_video], ignore_index=True)
            conn.update(worksheet="Videos", data=combined_data)
            
            st.success("Dados salvos na planilha!", icon="✅")
            st.balloons()
            st.rerun()
        else:
            st.warning("Por favor, adicione um vídeo ou uma URL.")

    # 5. Visualização Prévia
    if video_url_final or uploaded_video:
        with st.expander("Visualizar Prévia"):
            if uploaded_video:
                st.video(uploaded_video)
            elif video_url_final:
                st.video(video_url_final)
def galeria_videos():
    st.header("🎥 Galeria de Aulas")

    conn = st.connection("gsheets", type=GSheetsConnection)

    try:
        # ttl=0 evita cache para ver novos vídeos na hora
        df_videos = conn.read(worksheet="Videos", ttl=0)
    except Exception:
        st.error("Planilha 'Vídeos' não encontrada.")
        return

    if df_videos.empty:
        st.info("Nenhum vídeo cadastrado.")
        return

    # --- LIMPEZA DE DADOS ---
    # Remove linhas onde a URL do vídeo está totalmente vazia
    df_videos = df_videos.dropna(subset=['URL_Video'])
    # ------------------------

    materias = ["Todos"] + sorted(df_videos["Materia"].unique().tolist())
    selecao = st.selectbox("Filtrar por Matéria:", materias)

    df_filtrado = df_videos if selecao == "Todos" else df_videos[df_videos["Materia"] == selecao]

    st.divider()

    for index, row in df_filtrado.iterrows():
        # Verificação extra: garante que a URL é uma string e não está vazia
        video_url = row['URL_Video']

        if isinstance(video_url, str) and video_url.strip() != "":
            with st.container():
                col_video, col_info = st.columns([1.5, 1])

                with col_video:
                    st.video(video_url)

                with col_info:
                    # Usando .get() ou verificação simples para evitar erros de nomes de colunas
                    titulo = row.get('Titulo', 'Sem Título')
                    desc = row.get('Descrição', '')

                    st.subheader(titulo)
                    st.caption(f"📚 {row['Materia']}")
                    st.write(desc)

                st.divider()
        else:
            # Opcional: avisar que um vídeo está com link quebrado
            st.warning(f"O vídeo '{row.get('Titulo', index)}' está sem um link válido.")
        
def editar_video():
    st.header("✏️ Editar Vídeos com Pré-visualização")

    conn = st.connection("gsheets", type=GSheetsConnection)

    # 1. Carregar Dados da aba "Videos"
    try:
        df_videos = conn.read(worksheet="Videos", ttl=0).fillna("")
    except Exception as e:
        st.error(f"Erro ao acessar a aba 'Videos'. Verifique a planilha. Erro: {e}")
        return

    if df_videos.empty:
        st.info("Nenhum vídeo disponível para edição.")
        return

    # 2. Seleção do Vídeo
    titulos = df_videos["Titulo"].tolist()
    video_selecionado = st.selectbox("Selecione o vídeo para editar:", titulos)

    idx = df_videos[df_videos["Titulo"] == video_selecionado].index[0]
    dados_atuais = df_videos.iloc[idx]

    st.divider()

    # --- ÁREA DE PRÉ-VISUALIZAÇÃO DO QUE ESTÁ SALVO ---
    with st.expander("📺 Ver o vídeo que está salvo atualmente", expanded=False):
        if dados_atuais["URL_Video"]:
            st.video(dados_atuais["URL_Video"])
        else:
            st.warning("Sem link salvo.")
    
    st.divider()

    # --- LÓGICA DE SESSION STATE ---
    if "ultimo_video_selecionado" not in st.session_state or st.session_state["ultimo_video_selecionado"] != video_selecionado:
        st.session_state["ultimo_video_selecionado"] = video_selecionado
        st.session_state["draft_titulo"] = dados_atuais["Titulo"]
        st.session_state["draft_materia"] = dados_atuais["Materia"]
        st.session_state["draft_descricao"] = dados_atuais["Descrição"]
        st.session_state["draft_url"] = dados_atuais["URL_Video"]

    # --- FORMULÁRIO DE EDIÇÃO ---
    col_form1, col_form2 = st.columns(2)
    
    with col_form1:
        st.text_input("Título:", key="draft_titulo")
        
        # Bloco Try/Except para carregar matérias (CORRIGIDO)
        try:
            df_mat = conn.read(worksheet="Materias").fillna("")
            lista_mats = df_mat["Materia"].tolist()
            try:
                idx_mat_atual = lista_mats.index(st.session_state["draft_materia"])
            except ValueError:
                idx_mat_atual = 0
            
            st.selectbox("Matéria:", lista_mats, index=idx_mat_atual, key="draft_materia")
        except Exception:
            st.error("Erro ao carregar lista de matérias.")
            # Fallback caso a planilha de matérias falhe
            st.text_input("Matéria (digite manualmente):", key="draft_materia")

    with col_form2:
        st.text_area("Descrição:", height=115, key="draft_descricao")

    st.subheader("Alteração de Link e Preview")
    st.text_input("URL do Vídeo (YouTube/Link Direto):", key="draft_url")

    # Preview em tempo real
    with st.container(border=True):
        st.caption("Pré-visualização do novo link:")
        url_preview = st.session_state["draft_url"].strip()
        if url_preview:
            try:
                st.video(url_preview)
            except Exception:
                st.error("Não foi possível carregar o vídeo com este link.")
        else:
            st.info("Digite uma URL para ver o preview.")

    st.divider()

    # 4. Botões de Ação
    col_btn1, col_btn2, _ = st.columns([1, 1, 2])
    
    with col_btn1:
        if st.button("💾 Salvar Alterações", type="primary", use_container_width=True):
            df_videos.at[idx, "Titulo"] = st.session_state["draft_titulo"]
            df_videos.at[idx, "Materia"] = st.session_state["draft_materia"]
            df_videos.at[idx, "Descrição"] = st.session_state["draft_descricao"]
            df_videos.at[idx, "URL_Video"] = st.session_state["draft_url"]

            conn.update(worksheet="Videos", data=df_videos)
            st.success("Vídeo atualizado!")
            del st.session_state["ultimo_video_selecionado"]
            st.rerun()

    with col_btn2:
        if st.button("🗑️ Excluir Vídeo", use_container_width=True):
            df_videos = df_videos.drop(idx)
            conn.update(worksheet="Videos", data=df_videos)
            st.warning("Vídeo excluído.")
            del st.session_state["ultimo_video_selecionado"]
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
    import base64
    import requests
    import numpy as np
    import streamlit as st
    from streamlit_gsheets import GSheetsConnection
    import random
    
    # Conexão com a planilha
    conn = st.connection("gsheets", type=GSheetsConnection)
    existing_data = conn.read(worksheet="Questões", ttl=0)
    
    if existing_data.empty:
        st.warning("Nenhuma questão disponível para editar.")
        st.stop()
    
    # Inicializa embaralho se não existir
    if "embaralho" not in st.session_state:
        st.session_state["embaralho"] = random.sample(
            ["Alternativa_A", "Alternativa_B", "Alternativa_C", "Alternativa_D", "Alternativa_E"], 5
        )
    
    materias_unicas = existing_data["Materia"].unique()
    
    col1, col2 = st.columns(2)
    
    with col1:
        materia = st.selectbox("Matéria", options=materias_unicas)
    
    questoes_filtradas = existing_data[existing_data["Materia"] == materia]
    
    if questoes_filtradas.empty:
        st.warning(f"Nenhuma questão disponível para a matéria '{materia}'.")
        st.stop()
    
    with col2:
        questao_selecionada = st.selectbox(
            "Selecione a questão a editar:", 
            options=questoes_filtradas["Descrição"].tolist()
        )
    
    index = questoes_filtradas.index[questoes_filtradas["Descrição"] == questao_selecionada][0]
    questao_atual = questoes_filtradas.loc[index]
    
    descricao = st.text_input("Descrição", value=questao_atual["Descrição"], key=f"descricao_{index}")
    enunciado = st.text_area("Enunciado", value=questao_atual["Enunciado"], key=f"enunciado_{index}")
    alternativas = {
        "Alternativa_A": st.text_input("Resposta 1", value=questao_atual["Alternativa_A"], key=f"a_{index}"),
        "Alternativa_B": st.text_input("Resposta 2", value=questao_atual["Alternativa_B"], key=f"b_{index}"),
        "Alternativa_C": st.text_input("Resposta 3", value=questao_atual["Alternativa_C"], key=f"c_{index}"),
        "Alternativa_D": st.text_input("Resposta 4", value=questao_atual["Alternativa_D"], key=f"d_{index}"),
        "Alternativa_E": st.text_input("Resposta 5", value=questao_atual["Alternativa_E"], key=f"e_{index}")
    }
    
    st.subheader("Imagem da Questão")
    imagem_atual = questao_atual.get("Imagem", "")
    
    if imagem_atual:
        st.image(
            f"https://raw.githubusercontent.com/{st.secrets['github']['repo_owner']}/{st.secrets['github']['repo_name']}/main/imagens/{imagem_atual}",
            caption="Imagem Atual"
        )
    
        if st.button("Apagar imagem"):
            url = f"https://api.github.com/repos/{st.secrets['github']['repo_owner']}/{st.secrets['github']['repo_name']}/contents/imagens/{imagem_atual}"
            get_response = requests.get(url, headers={"Authorization": f"token {st.secrets['github']['token']}"})
            if get_response.status_code == 200:
                sha = get_response.json()["sha"]
                delete_payload = {
                    "message": f"Removendo {imagem_atual} via Streamlit",
                    "sha": sha,
                    "branch": st.secrets['github']['branch']
                }
                del_response = requests.delete(url, json=delete_payload, headers={"Authorization": f"token {st.secrets['github']['token']}"})
                if del_response.status_code == 200:
                    st.success("Imagem apagada com sucesso!")
                    existing_data.at[index, "Imagem"] = ""
                    conn.update(worksheet="Questões", data=existing_data)
                    st.rerun()
                else:
                    st.error("Erro ao apagar a imagem no GitHub.")
            else:
                st.warning("Imagem já não está presente no GitHub.")
    else:
        st.info("Questão sem imagem")
    
    uploaded_file = st.file_uploader("Atualizar imagem:", type=["jpg", "png", "jpeg"])
    
    with st.expander("Visualizar questão"):
        st.subheader('', divider='gray')
        # Enunciado
        st.write(f"**{enunciado}**")
        
        # Imagem (se existir)
        if imagem_atual:
            st.image(
                f"https://raw.githubusercontent.com/{st.secrets['github']['repo_owner']}/{st.secrets['github']['repo_name']}/main/imagens/{imagem_atual}",
                caption="Imagem da Questão"
            )
        st.subheader('', divider='gray')
        # Alternativas embaralhadas
        embaralho = st.session_state["embaralho"]
        opcoes = [alternativas[embaralho[i]] for i in range(5)]
        st.radio("Escolha uma opção:", options=opcoes, index=None)
        
    if st.button("Salvar alterações"):
        with st.spinner("Salvando..."):
            existing_data.at[index, "Descrição"] = descricao
            existing_data.at[index, "Enunciado"] = enunciado
            for alt_key in alternativas:
                existing_data.at[index, alt_key] = alternativas[alt_key]
    
            # Upload da imagem
            if uploaded_file:
                image_data = uploaded_file.getvalue()
                b64_content = base64.b64encode(image_data).decode("utf-8")
    
                url = f"https://api.github.com/repos/{st.secrets['github']['repo_owner']}/{st.secrets['github']['repo_name']}/contents/imagens/{uploaded_file.name}"
                payload = {
                    "message": f"Atualizando {uploaded_file.name} via Streamlit",
                    "content": b64_content,
                    "branch": st.secrets['github']['branch']
                }
                headers = {"Authorization": f"token {st.secrets['github']['token']}"}
    
                response = requests.put(url, json=payload, headers=headers)
    
                if response.status_code in (200, 201):  # 200 overwrite, 201 novo arquivo
                    existing_data.at[index, "Imagem"] = uploaded_file.name
                    st.success("Imagem atualizada com sucesso! 📤")
                else:
                    st.error(f"Erro ao atualizar a imagem: {response.json()}")
    
            conn.update(worksheet="Questões", data=existing_data)
            st.success("Questão editada com sucesso! ✅")
            st.rerun()


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
        conn.read(worksheet="Questões", ttl=0)

        st.toast(':green-background[Questão deletada com sucesso]', icon='✔️')
        st.rerun()
        # Atualiza cache para refletir a exclusão
        conn.read(worksheet="Questões", ttl=0)

        st.toast(':green-background[Questão deletada com sucesso]', icon='✔️')
        st.rerun()







































