import streamlit as st
from helper import get_QA_chain
from voice import azure_stt, azure_tts
import time

# Initialize QA chain
chain = get_QA_chain()
st.set_option('server.headless', True)
# Initialize session state variables
if 'is_voice' not in st.session_state:
    st.session_state['is_voice'] = False  # Track whether in voice mode
if 'is_speaking' not in st.session_state:
    st.session_state['is_speaking'] = False  # Track whether TTS is speaking

# Function to handle voice input (speech-to-text)
def process_voice_input():
    st.session_state['is_speaking'] = False
    audio_file = azure_stt()  # Use the function to get the voice input
    st.session_state['question'] = audio_file  # Update question from STT
    st.session_state['is_voice'] = True

    # Process the question and generate response
    response = get_response(st.session_state['question'])
    st.session_state['response'] = response["answer"]
    
    # Handle TTS (Text-to-Speech) response
    if st.session_state['is_voice']:
        azure_tts(st.session_state['response'])
        st.session_state['is_speaking'] = True

def get_response(question):
    chain = get_QA_chain()
    ans = chain.invoke({"input": question})
    return ans

# Streamlit frontend
st.title("The Hunar Foundation Bot")
st.sidebar.title("Toggle Chat Mode")
chat_mode = st.sidebar.radio("Select Chat Mode", ("Text Chat", "Voice Chat"))

# Handle toggle for voice or text chat mode
if chat_mode == "Text Chat":
    st.session_state['is_voice'] = False
    question = st.text_input("Ask a question: ")

    if question:
        response = get_response(question)
        st.write(response["answer"])

else:
    st.session_state['is_voice'] = True
    # Display button to start voice processing
    if st.button("Speak"):
        st.session_state['is_speaking'] = True
        process_voice_input()

    # Print the transcribed text and stop speaking if new speech is detected
    if st.session_state.get('question'):
        st.write(f"Your Question: {st.session_state['question']}")

    # Stop TTS if user speaks again or switches to text mode
    if st.session_state['is_speaking'] and chat_mode == 'Voice Chat' and st.session_state.get('response'):
        st.session_state['is_speaking'] = False
        time.sleep(1)  # Wait a moment to ensure TTS is completed before new input
