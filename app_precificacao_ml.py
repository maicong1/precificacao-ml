
import streamlit as st

# Configurações de página com favicon oficial e layout fullscreen
st.set_page_config(
    page_title="Calculadora ARJ",
    page_icon="favicon.ico",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS para mobile responsivo, fullscreen e layout compacto
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
        padding: 5px;
    }
    .stButton>button {
        width: 100%;
        padding: 0.8em;
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
        padding: 0.6em;
        border-radius: 6px;
        font-size: 1.1em;
    }
    .stMarkdown h1 {
        text-align: center;
        margin-bottom: 0.3em;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

# Apenas o título
st.title("Calculadora ARJ")

# Entradas do usuário com valores padrão
custo_unitario = st.number_input("Custo Unitário (R$)", min_value=0.0, format="%.2f")
comissao_ml = st.number_input("Comissão Marketplace (%)", min_value=0.0, max_value=30.0, value=0.0, format="%.2f")
frete = st.number_input("Custo de Envio (R$)", min_value=0.0, format="%.2f")
outros_custos = st.number_input("Outros Custos (R$)", min_value=0.0, format="%.2f")
markup_desejado = st.number_input("Markup desejado (%)", min_value=0.0, value=45.0, format="%.2f")

# Variável de estado para manter o preço editado
if "preco_editado" not in st.session_state:
    st.session_state.preco_editado = 0.0

# Botão calcular com largura total
if st.button("Calcular"):
    try:
        # Cálculo inicial
        preco_base = (custo_unitario + frete + outros_custos) / (1 - comissao_ml / 100)
        preco_sugerido = preco_base * (1 + markup_desejado / 100)
        st.session_state.preco_editado = preco_sugerido

    except ZeroDivisionError:
        st.error("❌ Comissão Marketplace não pode ser 100%")

# Campo para editar o preço sugerido
if st.session_state.preco_editado > 0:
    preco_editado = st.number_input(
        "💵 Preço Sugerido (edite para recalcular)", min_value=0.0,
        value=st.session_state.preco_editado, format="%.2f"
    )
    st.session_state.preco_editado = preco_editado

    # Recalcular com preço editado
    comissao_reais = preco_editado * (comissao_ml / 100)
    custo_total = custo_unitario + frete + outros_custos + comissao_reais
    lucro_bruto = preco_editado - custo_total
    margem_lucro = (lucro_bruto / preco_editado) * 100 if preco_editado else 0
    markup_real = ((preco_editado / (custo_unitario + frete + outros_custos)) - 1) * 100 if (custo_unitario + frete + outros_custos) else 0

    # Mostrar resultados
    col1, col2 = st.columns(2)
    col1.metric("Markup desejado", f"{markup_desejado:.2f}%")
    col2.metric("Markup real", f"{markup_real:.2f}%")

    st.info(f"📈 Lucro Bruto: R$ {lucro_bruto:.2f}")
    st.info(f"📊 Margem de Lucro: {margem_lucro:.2f}%")

st.caption("🔄 Desenvolvido pela ARJ Representações - Mobile First")
