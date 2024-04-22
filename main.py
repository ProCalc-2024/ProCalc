import streamlit as st

color = st.color_picker('Pick A Color', '#00f900')
st.write('The current color is', color)

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://img.hotimg.com/imgec6c25bbde259922.png");
background-size: cover;
}}

[data-testid="stHeader"] {{
background-color: rgba(0,0,0,0);
}}</style>
"""

st.sidebar.success("escolha uma das opções!")
st.write(r"""Resolva a expressão $$ a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} = \sum_{k=0}^{n-1} ar^k = a \left(\frac{1-r^{n}}{1-r}\right) $$ abaixo com o devido cuidado par simplificar utilizando os metodos adequados de agrupamento das expressões""")
st.latex(r''' a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} = \sum_{k=0}^{n-1} ar^k = a \left(\frac{1-r^{n}}{1-r}\right) ''')
