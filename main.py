import streamlit as st
from helper import get_QA_chain, folder_path

chain = get_QA_chain()

def get_response(question):
    chain = get_QA_chain()
    ans = chain.invoke({"input": question})
    return ans
    # print(ans)

       

st.title("The Hunar Foundation Chatbot Q&A 🌱")
question = st.text_input("Question: ")

if question:
    print(question)
    response = get_response(question)
    st.header("Answer")
    st.write(response["answer"])
    print(response['answer'])
