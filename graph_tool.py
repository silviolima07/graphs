from crewai_tools import tool
import pandas as pd
import lida
import os
import streamlit as st

@tool
def show_code(code:str):
    """
    Ferramenta que apresenta dados.
    """
    st.code(code, language='python')
    
@tool
def save_code(code:str, filename:str):
    """
    Ferramenta que salva códigos e análises geradas.
    """
    nome = f'{filename}'
    with open('output/'+nome, 'w') as file:
        st.write("Running tasks")
        file.write(code)   
    
@tool
def download_code(code:str, filename:str, formato:str):
    """
    Ferramenta que faz download dos códigos e análises.
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
    
@tool
def download_analise(analise:str, filename:str, formato:str):
    """
    Ferramenta que recebe dados em formato JSON, converte para pandas DataFrame,
    e gera gráficos usando a biblioteca LIDA.
    """
    # Suponha que o arquivo foi gerado no servidor
    output_file_content = analise

    # Nome do arquivo que o usuário verá para download
    output_file_name = f"{filename}.{formato}"
    
    try:
       # Adicionando um botão de download
       st.download_button(
       label="Baixar arquivo",
       data=output_file_content,
       file_name=output_file_name,
       mime="text/markdown" 
       )
       
       st.markdown('Download: '+output_file_name)   
    except:
            st.write("error no download")    
    

    

