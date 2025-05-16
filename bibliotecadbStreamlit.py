import streamlit as st
import re 


from sqlalchemy import create_engine
import pandas as pd
import os
import time

def conCursor():
#Connection e Cursor
    DATABASE_URL = os.environ["DATABASE_URL"]
    engine = create_engine(DATABASE_URL)

    # Para leitura e escrita com pandas
    return engine
    

def validar_email(email):
    padrao = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(padrao, email) is not None

def adicionar_no_DB(email,senha):
    engine = conCursor()
    adicionar = "INSERT INTO usuarios (email, senha) VALUES (%s, %s)"

    # Executando a consulta de inserção no banco
    with engine.connect() as conn:
        conn.execute(adicionar, (email, senha))  # Passando os parâmetros corretamente

    # Exibindo o feedback no Streamlit
    with st.empty():
        with st.spinner("Aguarde adicionando usuário..."):
            time.sleep(3)  # Simulando tempo de processamento
            st.success("Usuário Adicionado com Sucesso!")
    

def stpesq():

    email = st.text_input("Digite o email do usuario : ")


    senha = st.text_input("Digite a senha do usuario : ")
    

    if st.button("Adicionar usuario"):
        if not email or not senha:
            st.error("Erro : E-Mail ou Senha não foram inseridos.")
        elif not validar_email(email):
            st.error("Erro : O email não foi digitado de maneira correta.")
        else:
            adicionar_no_DB(email,senha)


def stdeletar():
    engine = conCursor()

    st.subheader("Qual e o id do usuario que deseja deletar? ")
    delid = st.number_input("ID da Tarefa :",min_value=1,step=1,label_visibility="collapsed")
    if st.button("Deletar Tarefa"):
        buscar = f"SELECT * FROM usuarios WHERE id = '{delid}'"

        resubusca = pd.read_sql(buscar,engine)
        if not resubusca.empty:
            st.warning("Tem certeza que deseja deletar esse usuario?Não será possivel recuperalo depois")
            if st.button("Sim eu tenho certeza."):
                with engine.begin() as conn:
                    conn.execute(f"DELETE FROM usuarios WHERE id = {delid}")
                    st.success("Usuario deletado com sucesso!")
        else:
            st.error("---Nennhum Usuario Encontrado---")


def stlistar():
    engine = conCursor()

    st.subheader("Lista de Usuarios : ")

    lista ="SELECT * FROM usuarios"

    listagem = pd.read_sql(lista,engine)

    if not listagem.empty:
        st.dataframe(listagem)
    else:
        st.error("Nenhum usuario cadastrado")


def stpri():
    
    with st.sidebar:

        escolha = st.selectbox("Qual ação deseja fazer?",("Adicionar novo usuario : ","Listar todos os usuarios : ","Deletar um usuario :  "))
        st.header("Qual ação deseja fazer?")
        add = st.button("Adicionar novo usuario : ")
        lista = st.button("Listar todos os usuarios : ")
        dele = st.button("Deletar um usuario :  ")
    if escolha == "Adicionar novo usuario : ":
        stpesq()
    elif escolha == "Listar todos os usuarios : ":
        stdeletar()
    elif escolha == "Deletar um usuario :  ":
        stlistar()
