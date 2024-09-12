from crewai_tools import tool
import pandas as pd
import os
import streamlit as st

@tool
def show_code(code:str):
    """
    Ferramenta que recebe dados em formato JSON, converte para pandas DataFrame,
    e gera gráficos usando a biblioteca LIDA.
    """
    st.code(code, language='python')
    
@tool
def download_code(code:str, filename:str, formato:str):
    """
    Ferramenta que recebe dados em formato JSON, converte para pandas DataFrame,
    e gera gráficos usando a biblioteca LIDA.
    """
    # Suponha que o arquivo foi gerado no servidor
    output_file_content = code

    # Nome do arquivo que o usuário verá para download
    output_file_name = f"{filename}.{formato}"
    
    try:
       # Adicionando um botão de download
       st.download_button(
       label="Baixar arquivo",
       data=output_file_content,
       file_name=output_file_name,
       mime="text/markdown"  )
       
       st.markdown('Download: '+output_file_name)   
    except:
            st.write("error no download")
    
    
    

    

