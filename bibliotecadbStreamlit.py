import streamlit as st
import re
from sqlalchemy import create_engine
import pandas as pd
import os
import time


def conCursor():
    "Conexão com o banco de dados usando a URL de conexão do Railway"
    DATABASE_URL = os.environ["DATABASE_URL"]
    engine = create_engine(DATABASE_URL)
    return engine


def validar_email(email):
    padrao = r"^[a-zA-Z0-9._%+-]+@[a-zAZ0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(padrao, email) is not None


def adicionar_no_DB(email, senha):
    engine = conCursor()
    adicionar = "INSERT INTO usuarios (email, senha) VALUES (%s, %s)"
    
    conn = engine.raw_connection()  
    cursor = conn.cursor() 
    
    cursor.execute(adicionar, (email, senha))  
    conn.commit()  

    cursor.close()  
    conn.close()  
    
    with st.empty():
        with st.spinner("Aguarde adicionando usuário..."):
            with time.sleep(3):  # Simulando tempo de processamento
                st.success("Usuário Adicionado com Sucesso!")
   
    

# Função de pesquisa e validação para adicionar o usuário
def stpesq():
    email = st.text_input("Digite o email do usuário: ")
    senha = st.text_input("Digite a senha do usuário: ")

    if st.button("Adicionar usuário"):
        if not email or not senha:
            st.error("Erro: E-Mail ou Senha não foram inseridos.")
        elif not validar_email(email):
            st.error("Erro: O email não foi digitado de maneira correta.")
        else:
            adicionar_no_DB(email, senha)

# Função para deletar um usuário
def stdeletar():
    engine = conCursor()

    st.subheader("Qual é o ID do usuário que deseja deletar? ")
    delid = st.number_input("ID do usuário:", min_value=1, step=1, label_visibility="collapsed")

    if st.button("Deletar usuário"):
        buscar = f"SELECT * FROM usuarios WHERE id = {delid}"

        resubusca = pd.read_sql(buscar, engine)
        if not resubusca.empty:
            st.warning("Tem certeza que deseja deletar esse usuário? Não será possível recuperá-lo depois.")
            if st.button("Sim, eu tenho certeza."):
                # Corrigindo para deletar da tabela 'usuarios'
                conn = engine.raw_connection()
                cursor = conn.cursor()
                cursor.execute(f"DELETE FROM usuarios WHERE id = {delid}")
                conn.commit()  # Commitando a transação

                cursor.close()  # Fechando o cursor
                conn.close()  # Fechando a conexão

                st.success("Usuário deletado com sucesso!")
        else:
            st.error("Nenhum usuário encontrado.")

# Função para listar todos os usuários
def stlistar():
    engine = conCursor()

    st.subheader("Lista de Usuários: ")

    lista = "SELECT * FROM usuarios"

    listagem = pd.read_sql(lista, engine)

    if not listagem.empty:
        st.dataframe(listagem)
    else:
        st.error("Nenhum usuário cadastrado.")

# Função principal para o menu
def stpri():
    with st.sidebar:
        st.subheader("Menu do Admin : ")
        escolha = st.selectbox("Qual ação deseja fazer?", ("Adicionar novo usuário", "Listar todos os usuários", "Deletar um usuário"))
        
    
    if escolha == "Adicionar novo usuário":
        stpesq()
    elif escolha == "Listar todos os usuários":
        stlistar()
    elif escolha == "Deletar um usuário":
        stdeletar()


