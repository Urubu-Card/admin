import bibliotecadbStreamlit as db
import streamlit as st


st.set_page_config(page_icon="❗",page_title="Adiconar Usuarios : ",layout="centered",)


st.session_state["deletar_confirmado"] = True


st.title("Gerenciador de Tarefas : ")

db.stpri()
