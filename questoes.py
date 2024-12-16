import streamlit as st

# Inicializar o estado, se necessário
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Aba 1"  # Defina o valor inicial

# Função para alterar o estado da aba ativa
def set_active_tab(tab_name):
    st.session_state.active_tab = tab_name

# Criar as abas
tabs = st.tabs(["Aba 1", "Aba 2", "Aba 3"])

# Verificar qual aba está ativa e exibir conteúdo
with tabs[0]:
    if st.session_state.active_tab == "Aba 1":
        set_active_tab("Aba 1")
    st.write("Você está na Aba 1")

with tabs[1]:
    if st.session_state.active_tab == "Aba 2":
        set_active_tab("Aba 2")
    st.write("Você está na Aba 2")

with tabs[2]:
    if st.session_state.active_tab == "Aba 3":
        set_active_tab("Aba 3")
    st.write("Você está na Aba 3")

# Forçar o redirecionamento para a aba ativa
selected_tab = st.session_state.active_tab
if selected_tab == "Aba 1":
    tabs[0].empty()
elif selected_tab == "Aba 2":
    tabs[1].empty()
elif selected_tab == "Aba 3":
    tabs[2].empty()
st.button("Say hello")
