import pandas as pd
from datetime import datetime
import plotly.express as px
import numpy as np
import streamlit as st

# Using plotly.express
import plotly.express as px


def value_human_readable(x):
    if x > 1_000_000:
        return str(round(x / 1_000_000, 2)) + " M"
    elif x < 1_000_000 and x > 1_000:
        return str(round(x / 1_000, 2)) + "K"
    else:
        return str(x)


def create_dataframe(data, min_val, min_date):
    top_x_clean = (
        data[data["Data de Celebração do Contrato"] > min_date]
        .groupby("Nome_tratado")
        .sum()
        .sort_values("CPV_VALOR_TRIM", ascending=False)
    )
    top_x_clean["CPV_VALOR_TRIM_HUMAN_READABLE"] = top_x_clean["CPV_VALOR_TRIM"].apply(
        lambda x: value_human_readable(x)
    )
    return top_x_clean.iloc[:min_val, -1].reset_index()


st.set_page_config(layout="wide")

data = pd.read_csv("data/original_data.csv", index_col=[0])

data["Data de Celebração do Contrato"] = pd.to_datetime(
    data["Data de Celebração do Contrato"]
)
st.header("Custos Informática Saúde")
st.markdown(
    """

"""
)
st.subheader("Top Empresas")
st.markdown(""" etc etc""")


vcol1, vcol2 = st.columns(2)


min_date = pd.to_datetime(vcol1.date_input("Limite Minimo", value=datetime(2014, 1, 1)))
min_val = vcol2.slider("Pick a minimum Ratio view per document", 1, 50, 20)

st.dataframe(create_dataframe(data, min_val, min_date))

st.subheader("Rubricas")
st.markdown(""" etc etc""")

ncol1, ncol2, ncol3 = st.columns(3)

empresas = list(data["Nome_tratado"].unique())

options = ncol1.multiselect("Filtrar por Empresa (NIF):", empresas, None)

view_col = [
    "Objeto do Contrato",
    "Tipo de Procedimento",
    "Tipo(s) de Contrato",
    "CPV",
    "CPV Designação",
    "CPV Valor",
    "Preço Contratual",
    "Preço Total Efetivo",
    "Data de Publicação",
    "Data de Celebração do Contrato",
    "Prazo de Execução",
    "Prazo_execução_nr",
    "Valor_Dia",
    "Fundamentação",
    "Procedimento Centralizado",
    "Nome_tratado",
    "CPV_VALOR_TRIM",
]

if len(options) == 0:
    if min_date:
        show_data = data[data["Data de Celebração do Contrato"] > min_date][view_col]
    else:
        show_data = data[view_col]
else:
    if min_date:
        show_data = data[
            (data["Nome_tratado"].isin(options))
            & (data["Data de Celebração do Contrato"] > min_date)
        ][view_col]
    else:
        show_data = data[data["Nome_tratado"].isin(options)][view_col]

ncol2.metric("Rows", len(show_data))
ncol3.metric("total Money", f'{round(show_data["CPV_VALOR_TRIM"].sum(), 2):,}')
st.dataframe(show_data)


fig = px.bar(
    show_data,
    x="Data de Celebração do Contrato",
    y="CPV_VALOR_TRIM",
    hover_data=["Objeto do Contrato", "Valor_Dia"],
)
st.plotly_chart(fig, use_container_width=True)
