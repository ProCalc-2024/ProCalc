import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import numpy as np

def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            
local_css(r"styles.css")

def inserir_ques():    
    
    with open('questoes.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    # adicionar uma nova pergunta
    result = {}

    n = 0

    col1, col2 = st.columns([1, 1])

    with col2:
        lista = [ linha for linha in config['questoes']['assuntos'] ]
        materia = st.selectbox("selecione uma materia",lista)

        for item in config['questoes']['assuntos'][materia]:
            n = n+1

    with col1:
        st.title("Questão " + str(n+1))

    result.update(config['questoes']['assuntos'][materia])

    config['questoes']['assuntos'][materia] = { n + 1 : {'enunciado':st.text_area("Enunciado", placeholder= "enunciado da questão"), 
                                                    'alternativa_a':st.text_input("Resposta1", placeholder= "resposta correta"), 
                                                    'alternativa_b':st.text_input("Resposta2", placeholder= "resposta2"), 
                                                    'alternativa_c':st.text_input("Resposta3", placeholder= "resposta3"), 
                                                    'alternativa_d':st.text_input("Resposta4", placeholder= "resposta4"), 
                                                    'alternativa_e':st.text_input("Resposta5", placeholder= "resposta5")
                                                    }
                                                }

    questao = config['questoes']['assuntos'][materia]

    result.update(questao)

    if st.button("Salvar"):

        config['questoes']['assuntos'][materia] = result

        with open('questoes.yaml', 'w') as file:
            yaml.dump(config, file)

        st.write(config['questoes']['assuntos'])

def inserir_assun():    
    
    with open('questoes.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    # adicionar uma nova pergunta
    result = {}

    st.title("Novo Assunto")

    result.update(config['questoes']['assuntos'])

    config['questoes']['assuntos'] = { st.text_area("assunto", placeholder= "digite aqui o assunto") : 
                                                {1 : 
                                                {'enunciado':"", 
                                                    'alternativa_a':"", 
                                                    'alternativa_b':"", 
                                                    'alternativa_c':"", 
                                                    'alternativa_d':"", 
                                                    'alternativa_e':""
                                                    }
                                                }
                                                }

    questao = config['questoes']['assuntos']

    result.update(questao)

    if st.button("Save"):

        config['questoes']['assuntos'] = result

        with open('questoes.yaml', 'w') as file:
            yaml.dump(config, file)

        st.write(config['questoes']['assuntos'])         
