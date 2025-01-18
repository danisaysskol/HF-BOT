import streamlit as st
from helper import get_QA_chain, folder_path
from voice import azure_stt, azure_tts

# Initialize session state variables
if "answer" not in st.session_state:
    st.session_state.answer = ""
if "chat_mode" not in st.session_state:
    st.session_state.chat_mode = "text"  # Default mode is "text"
if "question" not in st.session_state:
    st.session_state.question = ""

# Get QA chain
chain = get_QA_chain()

def get_response(question):
    """
    Get response from the QA chain.
    """
    chain = get_QA_chain()
    ans = chain.invoke({"input": question})
    return ans

def voice_chat():
    """
    Handle voice chat input and response.
    """
    st.write("Voice Chat Mode Active 🎙️")
    audio_file = st.file_uploader("Upload an audio file for your question (WAV/MP3):")
    if audio_file:
        st.write("Processing your audio...")
        question = azure_stt(audio_file)  # Convert speech to text
        st.write(f"Detected Question: {question}")
        st.session_state.question = question

        response = get_response(question)
        st.session_state.answer = response["answer"]

        st.write("Answer:")
        st.write(st.session_state.answer)

        # Convert text answer to speech
        audio_response = azure_tts(st.session_state.answer)
        st.audio(audio_response, format="audio/wav")

def text_chat():
    """
    Handle text chat input and response.
    """
    st.write("Text Chat Mode Active 💬")
    question = st.text_input("Type your question here:")
    if question:
        st.session_state.question = question
        response = get_response(question)
        st.session_state.answer = response["answer"]
        st.write("Answer:")
        st.write(st.session_state.answer)

# Title
st.title("The Hunar Foundation Chatbot Q&A 🌱")

# Sidebar for mode selection
st.sidebar.title("Chat Mode")
mode = st.sidebar.radio("Choose chat mode:", ("text", "voice"))
st.session_state.chat_mode = mode

# Handle mode switching
if st.session_state.chat_mode == "text":
    text_chat()
elif st.session_state.chat_mode == "voice":
    voice_chat()
