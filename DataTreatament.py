# Biblioteca para download dos dados:
import requests

# Bibliotecas para Tratamento dos dados:
#from tabula import read_pdf
import pandas as pd
import numpy as np
import pdfplumber


# Biblioteca para type hint:
from typing import List

# Funções ######################################################################
def download_data(download_url: str,
                             output_file: str = "planilhaInfluencers",
                             extension: str = ".pdf") -> str:
    """
    Função para baixar o conjunto de dados e extrair tabelas de um arquivo PDF.
    
    # Entrada:
    - download_url (string): URL de onde o PDF será baixado.
    - output_file (string): Caminho onde o arquivo será salvo (sem a extensão).
    - extension (string): Extensão do arquivo (default: ".pdf").
    
    # Saída:
    - path (string): Caminho completo onde o arquivo foi salvo.
    - tables (list): Lista de tabelas extraídas do PDF.
    """
    
    try:
        # Fazer a solicitação ao link para download
        response = requests.get(download_url, stream=True)
        response.raise_for_status()  # Verificar se houve erro na solicitação
        
        # Definir o caminho onde o PDF será salvo
        path = output_file + extension
        
        # Salvar o arquivo no diretório
        with open(path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # Filtrar chunks vazios
                    file.write(chunk)
        
        print(f"Arquivo baixado com sucesso: {path}")
        
        # Abrir o PDF usando pdfplumber para extrair as tabelas
        with pdfplumber.open(path) as pdf:
            tables = []
            for page in pdf.pages:
                table = page.extract_table()  # Extrair a tabela da página
                if table:
                    tables.append(table)  # Adicionar a tabela extraída à lista

        if tables:
            print(f"{len(tables)} tabela(s) extraída(s) com sucesso.")
        else:
            print("Nenhuma tabela encontrada no PDF.")
        
    except Exception as e:
        print(f"Erro ao baixar ou processar o arquivo: {e}")
        tables = []
    
    return path, tables  # Retorna o caminho do arquivo e as tabelas extraídas



def pdf_to_dataframe(pdf_path: str) -> pd.DataFrame:
    """
    Converte um arquivo PDF contendo tabelas em um DataFrame completo do pandas.

    Este processo extrai todas as tabelas do PDF e organiza as páginas em um único DataFrame.
    Inclui etapas para remover linhas desnecessárias, ajustar cabeçalhos e corrigir valores numéricos.

    Args:
        pdf_path (str): Caminho completo para o arquivo PDF.

    Returns:
        pd.DataFrame: DataFrame contendo os dados extraídos e organizados do PDF.

    Raises:
        Exception: Exceções podem ser levantadas durante o processamento de cada página.
    """

    # Extrai tabelas do PDF
    tables = read_pdf(pdf_path, pages="all", lattice=True) # 'lattice=True' funciona bem para tabelas com bordas; caso não funcione, tente 'stream=True'

    # Organiza a primeira página
    df = tables[0] # Dataframe

    # Remover a linha 0 e redefinir a linha 1 como cabeçalho
    df.columns = df.iloc[1]  # Define a linha 1 como cabeçalho
    df = df[2:]  # Remove a linha 0

    # Resetar o índice do DataFrame
    df.reset_index(drop=True, inplace=True)

    # Concatena o resto das páginas em dataframe
    for page in range(1,len(tables)):
      try:
        df_temp = tables[page].copy() # Precisa do copy para evitar erros

        # Limpando coluna errática
        if df_temp.shape[1] == 8:
          df_temp.drop("Unnamed: 0", axis=1, inplace = True) # Algumas tabelas surgem com uma coluna nula extra.

        """
        No processo de conversão de PDF para DataFrame, o pandas define
        a primeira linha como cabeçalho do DataFrame. Só que a primeira
        linha é dado. Então preciso fazer esse processo abaixo para
        trocar o cabeçalho de modo fazer a concatenação adequadamente
        sem perder a informação.
        """
        
        # Processo de troca de cabeçalho sem perder informação
        header_index = df_temp.shape[0]+1 # Definindo um index (+1 só pra garantir que não vai sobrescrever)
        df_temp.loc[header_index] = df_temp.columns # Duplicando a coluna nas linhas
        df_temp.columns = df.columns # Sobrescrevendo a coluna com a estrutura correta
        df_temp.reset_index(drop=True, inplace=True) # Reorganizando index

        # Concatena os dataframes
        df = pd.concat([df, df_temp]).copy()
        df.reset_index(drop=True, inplace=True) # Ajusta o index

      except Exception as e:
        print(f"Erro: {e}")
        print(page)

    # Corrige coluna de valores numéricos
    for i in range(len(df)):
        try:
            # Tentando converter o valor para inteiro
            df.loc[i, 'Qual a nota desse influ?'] = int(df.loc[i, 'Qual a nota desse influ?'])
        except ValueError:
            # Se der erro, substitui por NaN
            df.loc[i, 'Qual a nota desse influ?'] = np.nan

    return df

def read_csv(csv_path : str) -> pd.DataFrame:
   """
   Função apenas para ler o csv.
   """

   return pd.read_csv(csv_path)






    
