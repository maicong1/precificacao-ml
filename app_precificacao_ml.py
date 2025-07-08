
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
    st.session_state.historico = pd.DataFrame(columns=[
        "Produto", "Preço Premium (R$)", "Lucro Bruto Premium (R$)", "Margem Premium (%)", "Markup Real Premium (%)",
        "Preço Clássico (R$)", "Lucro Bruto Clássico (R$)", "Margem Clássico (%)", "Markup Real Clássico (%)"
    ])

st.title("Calculadora ARJ")

# Nome do produto obrigatório
produto_nome = st.text_input("📦 Nome do Produto")

# Entradas do usuário
custo_unitario = st.number_input("Custo Unitário (R$)", min_value=0.0, format="%.2f")
frete = st.number_input("Custo de Envio (R$)", min_value=0.0, format="%.2f")
outros_custos = st.number_input("Outros Custos (R$)", min_value=0.0, format="%.2f")
markup_desejado = st.number_input("Markup desejado (%)", min_value=0.0, value=45.0, format="%.2f")

# Variáveis de estado para preços editáveis
if "preco_premium" not in st.session_state:
    st.session_state.preco_premium = 0.0
if "preco_classico" not in st.session_state:
    st.session_state.preco_classico = 0.0

# Botão calcular
if st.button("Calcular") and produto_nome.strip() != "":
    try:
        custos_totais = custo_unitario + frete + outros_custos

        # Preço Premium (17% comissão)
        comissao_premium = 0.17
        preco_base_premium = custos_totais / (1 - comissao_premium)
        preco_premium = preco_base_premium * (1 + markup_desejado / 100)
        st.session_state.preco_premium = preco_premium

        # Preço Clássico (12% comissão)
        comissao_classico = 0.12
        preco_base_classico = custos_totais / (1 - comissao_classico)
        preco_classico = preco_base_classico * (1 + markup_desejado / 100)
        st.session_state.preco_classico = preco_classico

    except ZeroDivisionError:
        st.error("❌ Erro no cálculo.")

elif produto_nome.strip() == "":
    st.warning("⚠️ Informe o nome do produto para calcular.")

# Se preços foram calculados, mostrar campos editáveis e botão Recalcular
if st.session_state.preco_premium > 0 and st.session_state.preco_classico > 0:
    st.subheader("💎 Preço Premium vs. Preço Clássico")

    # Campos editáveis
    preco_premium_editado = st.number_input(
        "💵 Preço Premium (edite para recalcular)",
        min_value=0.0, value=st.session_state.preco_premium, format="%.2f"
    )
    preco_classico_editado = st.number_input(
        "💵 Preço Clássico (edite para recalcular)",
        min_value=0.0, value=st.session_state.preco_classico, format="%.2f"
    )

    # Botão Recalcular
    if st.button("Recalcular"):
        custos_totais = custo_unitario + frete + outros_custos

        # Premium
        comissao_reais_premium = preco_premium_editado * 0.17
        lucro_bruto_premium = preco_premium_editado - (custos_totais + comissao_reais_premium)
        margem_premium = (lucro_bruto_premium / preco_premium_editado) * 100 if preco_premium_editado else 0
        markup_real_premium = ((preco_premium_editado / custos_totais) - 1) * 100 if custos_totais else 0

        # Clássico
        comissao_reais_classico = preco_classico_editado * 0.12
        lucro_bruto_classico = preco_classico_editado - (custos_totais + comissao_reais_classico)
        margem_classico = (lucro_bruto_classico / preco_classico_editado) * 100 if preco_classico_editado else 0
        markup_real_classico = ((preco_classico_editado / custos_totais) - 1) * 100 if custos_totais else 0

        # Mostrar resultados atualizados
        col1, col2 = st.columns(2)
        with col1:
            st.metric("💵 Preço Premium", f"R$ {preco_premium_editado:.2f}")
            st.info(f"📈 Lucro Bruto: R$ {lucro_bruto_premium:.2f}")
            st.info(f"📊 Margem de Lucro: {margem_premium:.2f}%")
            st.info(f"📌 Markup Real: {markup_real_premium:.2f}%")
        with col2:
            st.metric("💵 Preço Clássico", f"R$ {preco_classico_editado:.2f}")
            st.info(f"📈 Lucro Bruto: R$ {lucro_bruto_classico:.2f}")
            st.info(f"📊 Margem de Lucro: {margem_classico:.2f}%")
            st.info(f"📌 Markup Real: {markup_real_classico:.2f}%")

        # Atualizar preços na sessão
        st.session_state.preco_premium = preco_premium_editado
        st.session_state.preco_classico = preco_classico_editado

        # Adicionar ao histórico
        st.session_state.historico = pd.concat([
            st.session_state.historico,
            pd.DataFrame([{
                "Produto": produto_nome,
                "Preço Premium (R$)": preco_premium_editado,
                "Lucro Bruto Premium (R$)": lucro_bruto_premium,
                "Margem Premium (%)": margem_premium,
                "Markup Real Premium (%)": markup_real_premium,
                "Preço Clássico (R$)": preco_classico_editado,
                "Lucro Bruto Clássico (R$)": lucro_bruto_classico,
                "Margem Clássico (%)": margem_classico,
                "Markup Real Clássico (%)": markup_real_classico
            }])
        ], ignore_index=True)

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
