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
        time.sleep(3)  
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

    # Inicializa 'deletar_confirmado' se não existir
    if 'deletar_confirmado' not in st.session_state:
        st.session_state.deletar_confirmado = False

    # Verificação e lógica de deletação
    if delid and st.button("Deletar usuário"):

        # Usando parâmetros na consulta SQL
        buscar = "SELECT * FROM usuarios WHERE id = %s"
        resubusca = pd.read_sql(buscar, engine, params=(delid,))

        if not resubusca.empty:
            # Mostra o estado atual de 'deletar_confirmado' para depuração
            st.write(f"deletar_confirmado (antes da confirmação): {st.session_state.deletar_confirmado}")

            # Pergunta para confirmação de exclusão
            st.warning("Tem certeza que deseja deletar esse usuário? Não será possível recuperá-lo depois.")
            
            # Verifica se o botão de confirmação foi clicado
            if st.button("Sim, eu tenho certeza."):
                # Atualiza o estado de 'deletar_confirmado' para True
                st.session_state.deletar_confirmado = True
                st.write(f"deletar_confirmado (depois da confirmação): {st.session_state.deletar_confirmado}")
                
                # Executa a deleção no banco de dados
                with engine.begin() as conn:
                    conn.execute("DELETE FROM usuarios WHERE id = %s", (delid,))
                    st.success("Usuário deletado com sucesso!")
        else:
            st.error("Usuário não encontrado.")
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


