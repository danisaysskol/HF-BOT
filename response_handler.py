from helper import get_QA_chain
import streamlit as st

def get_response(question):
    """Fetch response from the chatbot chain."""
    try:
        chain = get_QA_chain()
        response = chain.invoke({"input": question})
        return response
    except Exception as e:
        st.error("An error occurred while processing your request.")
        print(f"Error: {e}")
        return None
