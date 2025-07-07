
import streamlit as st

# Configurações de página com favicon oficial e layout fullscreen
st.set_page_config(
    page_title="Calculadora ARJ",
    page_icon="favicon.ico",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS para mobile responsivo e fullscreen sem rolagem
st.markdown(
    '''
    <style>
    html, body, [class*="css"]  {
        height: 100%;
        margin: 0;
        padding: 0;
        background-color: #0A1A2F;
        color: #FFFFFF;
        font-family: "Arial", sans-serif;
        overflow: hidden; /* Remove rolagem */
    }
    .stApp {
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 10px;
    }
    .stButton>button {
        width: 100%;
        padding: 1em;
        color: #FFFFFF;
        background-color: #000000;
        border-radius: 8px;
        border: none;
        font-size: 1.1em;
    }
    .stButton>button:hover {
        background-color: #333333;
    }
    .stNumberInput>div>div>input {
        background-color: #1E2A38;
        color: #FFFFFF;
        width: 100%;
        padding: 0.8em;
        border-radius: 6px;
        font-size: 1.1em;
    }
    .stMarkdown h1 {
        text-align: center;
        margin-bottom: 0.5em;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

# Título apenas
st.title("Calculadora ARJ")

# Entradas do usuário
custo_unitario = st.number_input("Custo Unitário (R$)", min_value=0.0, format="%.2f")
comissao_ml = st.number_input("Comissão Marketplace (%)", min_value=0.0, max_value=30.0, value=0.0, format="%.2f")
frete = st.number_input("Custo de Envio (R$)", min_value=0.0, format="%.2f")
outros_custos = st.number_input("Outros Custos (R$)", min_value=0.0, format="%.2f")
markup = st.number_input("Markup desejado (%)", min_value=0.0, value=45.0, format="%.2f")

# Botão calcular com largura total
if st.button("Calcular"):
    try:
        preco_base = (custo_unitario + frete + outros_custos) / (1 - comissao_ml / 100)
        preco_sugerido = preco_base * (1 + markup / 100)
        comissao_reais = preco_sugerido * (comissao_ml / 100)
        lucro_bruto = preco_sugerido - (custo_unitario + frete + outros_custos + comissao_reais)
        margem_lucro = (lucro_bruto / preco_sugerido) * 100 if preco_sugerido else 0

        st.success(f"💵 Preço Sugerido: R$ {preco_sugerido:.2f}")
        st.info(f"📈 Lucro Bruto: R$ {lucro_bruto:.2f}")
        st.info(f"📊 Margem de Lucro: {margem_lucro:.2f}%")
    except ZeroDivisionError:
        st.error("❌ Comissão Marketplace não pode ser 100%")

st.caption("🔄 Desenvolvido pela ARJ Representações - Mobile First")
