from crewai import Agent, Task, Crew, Process
from graph_tool import show_code, save_code, download_code, download_analise
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

# Função para remover arquivos do diretório output
def limpar_diretorio_output():
        output_dir = "output"
        arquivos = os.listdir(output_dir)
        for arquivo in arquivos:
            file_path = os.path.join(output_dir, arquivo)
            os.remove(file_path)
        


def download_file():
    """
    Ferramenta que recebe dados em formato JSON, converte para pandas DataFrame,
    e gera gráficos usando a biblioteca LIDA.
    """
    # Listar arquivos na pasta 'output' para download
    output_dir = "output"
    arquivos = os.listdir(output_dir)
    
    for arquivo in arquivos:
        with open(os.path.join(output_dir, arquivo), "rb") as file:
            st.download_button(
                label=f"Baixar {arquivo}",
                data=file,
                file_name=arquivo,
                mime="text/markdown" #if arquivo.endswith(".py") else "text/markdown"
            )
    limpar_diretorio_output()
    #st.session_state.processed = False
    st.markdown("###### Mensagens serão removidas após download")     

img = Image.open("img/robo.png")
st.sidebar.image(img,caption="",use_column_width=True)

st.sidebar.markdown("# Menu")
option = st.sidebar.selectbox("Menu", ["Upload", 'About'], label_visibility='hidden')

# Verificar se o processamento já foi realizado (utilizando session_state)

#st.write("Begin - session_state.processed:",st.session_state)

if "processed" not in st.session_state or st.session_state.processed == True:
    st.session_state.processed = False

#st.write("After - session_state.processed:",st.session_state.processed)
n = 0
if option == 'Upload':
    html_page_title = """
     <div style="background-color:black;padding=60px">
         <p style='text-align:center;font-size:50px;font-weight:bold'>Gerador de Gráficos</p>
     </div>
               """               
    st.markdown(html_page_title, unsafe_allow_html=True)
    # Usar Streamlit para mostrar a interface
    st.markdown("### CrewAI: Agente Especialista de Visualização")

    st.markdown("## Upload CSV")
    uploaded_file = st.file_uploader("Envie o seu arquivo em CSV", type=["csv"])

    #if uploaded_file is not None:
    if uploaded_file is not None and not st.session_state.processed:
    
        
        # Obter o nome do arquivo
        file_name = uploaded_file.name
    
        # Separar o nome do arquivo da extensão
        file_name_without_ext, file_extension = os.path.splitext(file_name)
    
        # Exibir os resultados
        st.markdown("### Nome do arquivo: "+file_name_without_ext)
        #st.write("Extensão do arquivo:", file_extension)
    
        # Criar o agente CrewAI que vai analisar os dados
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
    'Gráficos como histograma, boxplot, dispersão, pizza, barros devem ter os códigos criados e incluídos na análise final.'
    'Análise de correlação, ranking e estáticas de dados ausentes devem ser incluídos na análise final.'
    'Apresentar análise com as explicações de cada coluna usada nos gráficos e qual conhecimento pode ser obtido a partir do gráfico devem estar na resposta final e no arquivo final.'
    'Apresentar junto com a análise e explicações, os códigos dos gráficos propostos.'
    'A mesma resposta final apresentada na saída deve estar na arquivo final gerado'
    'Exatamente os mesmos textos de códigos, texto de explicações e texto de conclusão apresentada na resposta final deve estar no arquivo final.'
    #'#Informar que os codigos gerados estão no arquivo {filename} formato python.'
    #'Por último, todos os códigos python gerados e a análise gerada devem ser salvos com a ferramenta save_code.'
    #'Usar save_code para salvar código com nome {filename}{formato_markdown}.'
    #'Usar save_code para salvar códigos e análise com nome analise_{filename}{formato_markdown}.'
    ,
        agent=data_visualizer,
        expected_output=
             "Apresentar análise com as explicações das colunas e graficos, nao deve mostrar imagens ou codigo e  deve em formato Markdown. Apenas explicar o objetivo do gráfico gerado.Um texto claro, em Português do Brasil."
             #"Usar a ferramenta para baixar a análise num arquivo formato {formato_markdown}."
             ,
        output_file= 'output/analise_'+f"{file_name_without_ext}.md"       
        #tools=[save_code]
    
        )
        
            
        # Criar o agente CrewAI que vai revisar e baixar os dados
        data_revisor = Agent(
    role='Data Visualizer',
    goal='revisar dados e baixar analises e codigos.',
    verbose=True,
    backstory=(
     "Você é um especialista em Python."
     "Seu trabalho é revisar as analises e codigos python gerados."
     "Você deve checar se análises e códigos estão perfeitos e depois baixar os dados usando a ferramenta."
        ),
    llm=llama
         )
        # Criar a task que descreve o que o agente deve fazer
        revision_task = Task(
        description=
    'Revisar as analises feitas para garantir o entendimentos dos dados.'
    'Revisar os códigos python gerados para garantir que possam ser executados sem erros.'
    'Usar a ferramenta download_code para baixar o código com nome {filename} formato {formato_python}.'
    'Salvar a análise com nome analise_{filename} formato {formato_markdown}.'
    ,
        agent=data_revisor,
        expected_output=
             "Apresentar análise com as explicações das colunas e graficos, nao deve mostrar imagens ou codigo e  deve em formato Markdown. Apenas explicar o objetivo do gráfico gerado.Um texto claro, em Português do Brasil."
             #"Usar a ferramenta para baixar a análise num arquivo formato {formato_markdown}."
             ,
        output_file= 'output/'+f"{file_name_without_ext}.md" ,       
        tools=[download_code, download_analise]
    
        )

        # Criar o Crew
        crew = Crew(
        agents=[data_visualizer],# , data_revisor],
        tasks=[visualization_task], #, revision_task],
        process=Process.sequential  # Executa as tarefas de forma sequencial
        )
        

        
        
        # Ler o dataset e exibir as primeiras linhas
        data = pd.read_csv(uploaded_file)
        st.write("Dataset lido")
        data = data.drop(columns=['Unnamed: 0'], errors='ignore')
        st.table(data.head(3))
            
        colunas = data.columns
        lista_colunas = colunas.to_list()
        
        if st.button("Processar dados"):
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
                
                    # Marcar que o processamento foi concluído
                    st.session_state.processed = True
                
                
                except:
                    st.write("error no crew.kickoff")
            #st.write("After - session_state.processed:",st.session_state.processed)
        
            # Verificar se o processamento foi concluído
            if st.session_state.processed:
                st.success("O processamento foi concluído! Pronto para download do arquivo com análise.")
                download_file()
            
      
    
if option == 'About':
    #st.markdown("## CrewAI")
    html_page_about = """
     <div style="background-color:black;padding=60px">
         <p style='text-align:center;font-size:50px;font-weight:bold'>CrewAI</p>
     </div>
               """               
    st.markdown(html_page_about, unsafe_allow_html=True)
    
    st.markdown("### Agente Especialista de Visualização")
    st.markdown("### Task: Analisar e propor gráficos que auxiliem o entendimento dos dados.")
    st.markdown("### Este aplicativo faz uma análise dos dados de um dataset.")
    st.markdown("### A análise pode ser baixada no final do processamento.")
    st.markdown("### Não substitue uma análise mais profunda com base no entendimento das regras do negócio.")
    

    
