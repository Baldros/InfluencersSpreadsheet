# Bibliotecas para visualização de dados:
from matplotlib import pyplot as plt
import pandas as pd

# Biblioteca para Web Aplication:
import streamlit as st

# Funções utilizadas ###########################################################
def plot_influencer(influencer: str, dataframe: pd.DataFrame) -> None:
    # Filtrar o DataFrame para o influenciador específico
    df_temp = dataframe[dataframe["Nome do influencer"] == influencer]

    # Contar o número de vezes que o influenciador aparece por nota
    nota_counts = df_temp["Qual a nota desse influ?"].value_counts().sort_index()

    # Exibir gráfico de barras no Streamlit usando st.bar_chart
    st.bar_chart(nota_counts)


def grafico_geral(dataframe):
    # Calcular as frequências de cada nota
    counts = dataframe["Qual a nota desse influ?"].value_counts().sort_index()

    # Exibir o gráfico de barras com Streamlit
    st.bar_chart(counts)

def experiencia_com_influencer(influencer : str, dataframe: pd.DataFrame):

  textos = []
  qtd_experiencias = dataframe[dataframe["Nome do influencer"]==influencer]["Como foi trabalhar com esse influ?"].shape[0]
  qtd_conselhos = dataframe[dataframe["Nome do influencer"]==influencer]["Conselho p/ colegas da área"].shape[0]

  for i in range(qtd_experiencias):
    try:
      textos.append("* **Experiência:**\n" + dataframe[dataframe["Nome do influencer"]==influencer]["Como foi trabalhar com esse influ?"].iloc[i])
    except:
      pass

    try:
      textos.append("* **Conselho para Colegas:**\n" + dataframe[dataframe["Nome do influencer"]==influencer]["Conselho p/ colegas da área"].iloc[i])
    except:
      pass

  return textos

def read_text(texto : str, tratamento : str = "\n")->str:

  #for texto in textos:
  texto = texto.replace('\r', tratamento) # Removendo todos os caracteres \r
  return texto

def table_pontuation(dataframe):
    # Calcular soma e contagem de notas por influenciador
    tabela = dataframe.groupby("Nome do influencer", as_index=False).agg(
       Pontuação_Total=("Qual a nota desse influ?", "sum"),
       Ocorrências=("Qual a nota desse influ?", "count")
    )

    # Calcular a pontuação média
    #tabela["Pontuação Média"] = tabela["Pontuação_Total"] / tabela["Ocorrências"]

    # Ordenando tabela:
    tabela.sort_values("Pontuação_Total",inplace=True)
    tabela.reset_index(drop=True, inplace=True)

    return tabela

