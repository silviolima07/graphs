from crewai import Agent, Task, Crew, Process
from graph_tool import show_code, download_code
import pandas as pd
import streamlit as st
import os
import os
from dotenv import load_dotenv
import pandas as pd
import warnings
from config_llm import llama

from PIL import Image
warnings.filterwarnings("ignore", category=UserWarning)
# Suprimir avisos específicos
warnings.filterwarnings("ignore", message="Overriding of current TracerProvider is not allowed")


from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

# Definir um TracerProvider que não coleta dados
trace.set_tracer_provider(TracerProvider())

# Desabilitar o TracerProvider (basicamente sem definir um novo)
trace.set_tracer_provider(None)

load_dotenv()


html_page_title = """
     <div style="background-color:black;padding=60px">
         <p style='text-align:center;font-size:50px;font-weight:bold'>Gerador de Gráficos</p>
     </div>
               """               
st.markdown(html_page_title, unsafe_allow_html=True)
# Usar Streamlit para mostrar a interface
st.markdown("### CrewAI: Agente Especialista de Visualização")
st.markdown("### Task: Analisar e propor gráficos que auxiliem o entendimento dos dados.")

img = Image.open("img/robo.png")
st.sidebar.image(img,caption="",use_column_width=True)

st.sidebar.markdown("# Menu")
option = st.sidebar.selectbox("Menu", ["Upload", 'About'], label_visibility='hidden')


if option == 'Upload':
    st.markdown("## Upload CSV")
    uploaded_file = st.file_uploader("Envie o seu arquivo em CSV", type=["csv"])

    if uploaded_file is not None:
        # Obter o nome do arquivo
        file_name = uploaded_file.name
    
        # Separar o nome do arquivo da extensão
        file_name_without_ext, file_extension = os.path.splitext(file_name)
    
        # Exibir os resultados
        st.markdown("### Nome do arquivo: "+file_name_without_ext)
        #st.write("Extensão do arquivo:", file_extension)
    
        # Criar o agente CrewAI que vai utilizar a ferramenta LIDA
        data_visualizer = Agent(
    role='Data Visualizer',
    goal='Interpretar dados e gerar gráficos.',
    verbose=True,
    backstory=(
     "Você é um especialista em visualização de dados."
     "Seu trabalho é analisar conjuntos de dados, entender suas propriedades e gerar gráficos relevantes."
        ),
        llm=llama
         )

    
        # Criar a task que descreve o que o agente deve fazer
        visualization_task = Task(
        description=
    'Explicar o dataset a partir das colunas em {lista_colunas}'
    'Gerar o código python usando as melhores lib para gerar uma visualização dos dados.'
    'Gráficos como histograma, boxplot, dispersão, pizza, barros, etc...devem ter os códigos criados.'
    'Análise de correlação, ranking e estáticas de dados ausentes, com problema, etc...devem ser incluídos no código criado. .'
    'Apresentar análise com as explicações apenas. Informar que os codigos gerados estão no arquivo {filename} formato python.'
    'Usar ferramenta para baixar o código com nome {filename} formato {formato_python}.'
    ,
        agent=data_visualizer,
        expected_output=
             "Apresentar análise com as explicações das colunas e graficos, nao deve mostrar imagens ou codigo e  deve em formato Markdown. Apenas explicar o objetivo do gráfico gerado.Um texto claro, em Português do Brasil."
             "Usar a ferramenta para baixar a análise num arquivo formato {formato_markdown}.",
    #output_file= 'output/'+f"{file_name_without_ext}.md" ,       
        tools=[download_code]
    
        )

        # Criar o Crew
        crew = Crew(
        agents=[data_visualizer],
        tasks=[visualization_task],
        process=Process.sequential,
        verbose=False,
        max_rpm=30        # Executa as tarefas de forma sequencial
        )

        if uploaded_file is not None:
            data = pd.read_csv(uploaded_file)
            st.write("Dataset lido")
            # Remover a coluna 'Unnamed: 0', se ela existir
            data = data.drop(columns=['Unnamed: 0'], errors='ignore')
            st.table(data.head(3))
            
            colunas = data.columns
            lista_colunas = colunas.to_list()
            st.markdown("### Aguarde o fim do processamento para baixar os arquivos.")
             
        with st.spinner('Wait for it...all data are been analysed...graph codes been building'):
            # Executa o CrewAI
            try:
                result = crew.kickoff(inputs={'lista_colunas': lista_colunas, 'filename': file_name_without_ext, 'formato_python': '.py', 'formato_markdown': '.md'})              
                
                html_page_result = """
     <div style="background-color:black;padding=60px">
         <p style='text-align:center;font-size:40px;font-weight:bold'>Resultado</p>
     </div>
               """               
                st.markdown(html_page_result, unsafe_allow_html=True)
                
                st.write(result.raw)
                
                
            except:
                st.write("error no crew.kickoff")
    
if option == 'About':
    #st.markdown("# About:")
    st.markdown("### Este aplicativo faz uma análise dos dados de um dataset.")
    st.markdown("### Um agente Especialista em Visualização deve  efetuar uma análise e propor gráficos.")
    st.markdown("### O objetivo é criar gráficos que permitam entender melhor o conjunto de dados.")
    st.markdown("### O código dos gráficos e a análise podem ser baixados ao final do processamento.")
    

    
