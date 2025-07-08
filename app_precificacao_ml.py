
import streamlit as st
import pandas as pd

# Configurações de página
st.set_page_config(
    page_title="Calculadora ARJ",
    page_icon="favicon.ico",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS para dashboard mobile
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
    .stNumberInput>div>div>input, .stTextInput>div>div>input {
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

# Inicializar histórico na sessão
if "historico" not in st.session_state:
    st.session_state.historico = pd.DataFrame(columns=["Produto", "Preço Sugerido (R$)", "Lucro Bruto (R$)", "Margem (%)", "Markup Real (%)"])

st.title("Calculadora ARJ")

# Nome do produto obrigatório
produto_nome = st.text_input("📦 Nome do Produto")

# Entradas do usuário
custo_unitario = st.number_input("Custo Unitário (R$)", min_value=0.0, format="%.2f")
comissao_ml = st.number_input("Comissão Marketplace (%)", min_value=0.0, max_value=30.0, value=0.0, format="%.2f")
frete = st.number_input("Custo de Envio (R$)", min_value=0.0, format="%.2f")
outros_custos = st.number_input("Outros Custos (R$)", min_value=0.0, format="%.2f")

# Escolha se quer calcular pelo markup ou preço sugerido
modo = st.radio("Modo de cálculo:", ["Usar Markup para calcular Preço", "Usar Preço para calcular Markup"])

if modo == "Usar Markup para calcular Preço":
    markup_desejado = st.number_input("Markup desejado (%)", min_value=0.0, value=45.0, format="%.2f")
else:
    preco_editado = st.number_input("Preço Sugerido (R$)", min_value=0.0, format="%.2f")

# Botão calcular
if st.button("Calcular") and produto_nome.strip() != "":
    try:
        custos_totais = custo_unitario + frete + outros_custos
        preco_base = (custos_totais) / (1 - comissao_ml / 100)

        if modo == "Usar Markup para calcular Preço":
            preco_sugerido = preco_base * (1 + markup_desejado / 100)
        else:
            preco_sugerido = preco_editado

        comissao_reais = preco_sugerido * (comissao_ml / 100)
        lucro_bruto = preco_sugerido - (custos_totais + comissao_reais)
        margem_lucro = (lucro_bruto / preco_sugerido) * 100 if preco_sugerido else 0
        markup_real = ((preco_sugerido / custos_totais) - 1) * 100 if custos_totais else 0

        # Mostrar resultados em cards
        col1, col2, col3 = st.columns(3)
        col1.metric("💵 Preço Sugerido", f"R$ {preco_sugerido:.2f}")
        col2.metric("📈 Lucro Bruto", f"R$ {lucro_bruto:.2f}")
        col3.metric("📊 Margem de Lucro", f"{margem_lucro:.2f}%")
        st.metric("📌 Markup Real", f"{markup_real:.2f}%")

        # Adicionar ao histórico
        st.session_state.historico = pd.concat([
            st.session_state.historico,
            pd.DataFrame([{
                "Produto": produto_nome,
                "Preço Sugerido (R$)": preco_sugerido,
                "Lucro Bruto (R$)": lucro_bruto,
                "Margem (%)": margem_lucro,
                "Markup Real (%)": markup_real
            }])
        ], ignore_index=True)

    except ZeroDivisionError:
        st.error("❌ Comissão Marketplace não pode ser 100%")
elif produto_nome.strip() == "":
    st.warning("⚠️ Informe o nome do produto para calcular.")

# Botão Resetar
if st.button("Resetar"):
    st.experimental_rerun()

# Histórico e download
if not st.session_state.historico.empty:
    st.subheader("📖 Histórico de Cálculos")
    st.dataframe(st.session_state.historico, use_container_width=True)
    csv = st.session_state.historico.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Baixar Histórico (CSV)", data=csv, file_name="historico_calculos_arj.csv", mime="text/csv")

st.caption("🔄 Desenvolvido pela ARJ Representações - Mobile First")
