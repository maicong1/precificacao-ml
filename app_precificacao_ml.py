
import streamlit as st

st.title("Calculadora de Precificação - Mercado Livre")

st.write("Preencha os campos abaixo para calcular o preço sugerido, lucro bruto e margem de lucro.")

# Entradas do usuário
custo_unitario = st.number_input("Custo Unitário (R$)", min_value=0.0, format="%.2f")
markup = st.number_input("Markup (%)", min_value=0.0, format="%.2f")
comissao_ml = st.number_input("Comissão Mercado Livre (%)", min_value=0.0, max_value=20.0, value=12.0, format="%.2f")
frete = st.number_input("Custo de Envio (R$)", min_value=0.0, format="%.2f")
outros_custos = st.number_input("Outros Custos (R$)", min_value=0.0, format="%.2f")

if st.button("Calcular"):
    preco_sugerido = custo_unitario * (1 + markup / 100) + frete + outros_custos
    comissao_reais = preco_sugerido * (comissao_ml / 100)
    lucro_bruto = preco_sugerido - (custo_unitario + comissao_reais + frete + outros_custos)
    margem_lucro = (lucro_bruto / preco_sugerido) * 100 if preco_sugerido else 0

    st.success(f"Preço Sugerido: R$ {preco_sugerido:.2f}")
    st.info(f"Lucro Bruto: R$ {lucro_bruto:.2f}")
    st.info(f"Margem de Lucro: {margem_lucro:.2f}%")

st.caption("💡 Desenvolvido para vendedores do Mercado Livre")
