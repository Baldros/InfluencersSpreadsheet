# Bibliotecas 
import streamlit as st
from DataTreatament import *
from EDAInfluencers import *

# Função para download com cache
@st.cache_data
def get_data_from_url():
    """
    Faz o download dos dados apenas uma vez e os retorna.
    """

    # Importando os dados:
    try:
       # url da pagina:
       url = f"https://drive.google.com/uc?id=1oq1nPOKMWAHCCdRzlRJZsaKFsgrrDmjH&export=download"

       # Download dos dados:
       path = download_data(url)

       # Tratamento dos dados:
       dataframe = pdf_to_dataframe(path)

       return dataframe
    
    except Exception as e:
       print(f"Erro: {e}")
       print("""
             No respectivo github consta os dados tabelados.
             
             https://github.com/Baldros/InfluencersSpreadsheet/tree/main
             """)
       
       return None
    
# Função para exibir os DataFrames lado a lado
def show_dataframes_side_by_side(df1, df2):
    # Criando duas colunas lado a lado
    col1, col2 = st.columns(2)

    # Exibindo o primeiro dataframe na coluna da esquerda
    with col1:
        st.subheader("Piores Influenciadores")
        st.dataframe(df1)

    # Exibindo o segundo dataframe na coluna da direita
    with col2:
        st.subheader("Melhores Influenciadores")
        st.dataframe(df2)

# Função Principal:
def main(dataframe : pd.DataFrame = None):
    """
    Função de construção do app de streamlit.
    """

    # Apresentação do Projeto:
    st.title("Planilha dos Influencers")
    st.write("""
            Recentemente, uma planilha contendo avaliações anônimas de profissionais de marketing
            sobre influenciadores e celebridades brasileiras vazou nas redes sociais, gerando ampla
            repercussão. O objetivo aqui é justamente dar uma explorada nessa planilha e ver o que
            de interessante foi dito.
            """)
    st.header("Nota:")
    st.write("""
            A intenção desse projeto não é ofender nem atacar ninguém de modo que apenas utiliza de
            um assunto do momento para justificar o estudo de soluções na área da tecnologia.
            """)
    
    # Correção (Caso haja problemas em baixar o arquivo):
    if dataframe is None:
        st.header("Upload de Arquivo")
        st.write("""
                Acesse a seguinte página para ter acesso ao conjunto de dados.
                 
                https://github.com/Baldros/InfluencersSpreadsheet/blob/main/influenciadores.csv
                """)
        upload_file = st.file_uploader("Escolha um arquivo", type=["pdf", "csv"], key="file_uploader_1")

        print(dir(upload_file))

        if upload_file is not None:
            # Criar um caminho temporário
            dataframe = pd.read_csv(upload_file)



    # Iniciando Análise:
    if dataframe is not None:
        
        st.header("Influenciadores")
        st.write("""
                 Vamos iniciar a análise da planilha. Todo o processo é bem intuitivo,
                 divirta-se.
                 """)
        # Visualização do DataFrame
        check_box_dataframe = st.checkbox("Visualização do DataFrame",value=True)
        if check_box_dataframe:
            st.dataframe(dataframe)  # Exibe um DataFrame interativo

        # Distribuição Geral das Pontuações
        check_box_geral = st.checkbox("Distribuição Geral das Pontuações:",value=True)
        if check_box_geral:
            grafico_geral(dataframe)

        # Select Box para selecionar o influenciador:
        influencers = dataframe["Nome do influencer"].unique() # lista de influenciadores
        selected_influencer = st.selectbox("Selecione uma opção",influencers) # Setando os influencers nas opções de seleção

        if selected_influencer:
            textos = experiencia_com_influencer(selected_influencer,dataframe)
            for texto in textos:
                st.write(read_text(texto))

        # Visualizações:
        st.subheader("Pontuação")
        if selected_influencer:
            plot_influencer(selected_influencer, dataframe)


        # Encontrar o pior ou melhor:
        st.header("Rankeamento")
        st.write("""
                 Talvez você esteja curioso em entender quem é o melhor, ou
                 o pior influencer... Segundo o construtores 
                 da planilha. Aqui vamos resolver essa questão.
                 """)
        value = st.number_input("Digite a quantidade de pessoas no rank: ", min_value=1,max_value=dataframe.shape[0]//2)
        if st.button("Piores e Melhores"):
            tabela_pontuacao = table_pontuation(dataframe) # Pegando a pontuação
            #st.dataframe(tabela_pontuacao)  # Exibe um DataFrame interativo
            piores = tabela_pontuacao[:value]
            melhores = tabela_pontuacao.sort_values("Pontuação_Total", ascending=False)
            melhores = melhores.reset_index(drop=True)[:value]
            #st.dataframe(piores)
            #st.dataframe(melhores)
            show_dataframes_side_by_side(piores,melhores)




        # Feedback:
        st.feedback("thumbs")
        


        # Votação:
        
    
if __name__ == "__main__":

    # Importando os dados apenas uma vez
    df = get_data_from_url()
    main(df)