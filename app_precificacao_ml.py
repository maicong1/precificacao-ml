
import streamlit as st

# Configurações de página com cor de fundo
st.set_page_config(
    page_title="Calculadora ARJ",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="auto"
)

# Custom CSS para cores e estilo minimalista
st.markdown(
    '''
    <style>
    body {
        background-color: #0A1A2F;
        color: #FFFFFF;
    }
    .stButton>button {
        color: #FFFFFF;
        background-color: #000000;
    }
    .stButton>button:hover {
        background-color: #333333;
        color: #FFFFFF;
    }
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #1E2A38;
        color: #FFFFFF;
    }
    .css-1v3fvcr { color: #FFFFFF; }
    </style>
    ''',
    unsafe_allow_html=True
)

# Título e descrição
st.title("Calculadora ARJ")
st.write("Use a Calculadora ARJ para definir preços com precisão e transparência, considerando todas as taxas e custos operacionais dos marketplaces.")

# Entradas do usuário
custo_unitario = st.number_input("Custo Unitário (R$)", min_value=0.0, format="%.2f")
comissao_ml = st.number_input("Comissão Marketplace (%)", min_value=0.0, max_value=30.0, value=12.0, format="%.2f")
frete = st.number_input("Custo de Envio (R$)", min_value=0.0, format="%.2f")
outros_custos = st.number_input("Outros Custos (R$)", min_value=0.0, format="%.2f")
markup = st.number_input("Markup desejado (%)", min_value=0.0, format="%.2f")

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
st.caption("🔄 Desenvolvido pela ARJ Representações")
