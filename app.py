import streamlit as st
from main import create_vector_db, get_qa_chain
st.set_page_config(page_title= 'QnA app')

st.title("Edtech QnA :mag:")

btn = st.button("Create Knowledgebase")
if btn:
    pass

question = st.text_input("Question")
if question:
    chain = get_qa_chain()
    response = chain(question)

    st.header("Answer")
    st.info(response["result"])