import streamlit as st
from helper import get_QA_chain
from voice import azure_stt, azure_tts
import time

# Initialize QA chain
chain = get_QA_chain()

# Initialize session state variables
if 'is_voice' not in st.session_state:
    st.session_state['is_voice'] = False  # Track whether in voice mode
if 'is_speaking' not in st.session_state:
    st.session_state['is_speaking'] = False  # Track whether TTS is speaking
if 'question' not in st.session_state:
    st.session_state['question'] = None  # Store the transcribed question
if 'audio_response' not in st.session_state:
    st.session_state['audio_response'] = None  # Store the audio response

# Function to process recorded audio input
def process_audio_input(audio_file):
    st.session_state['is_speaking'] = False

    # Save the audio to a temporary file
    temp_audio_path = "temp_audio.wav"
    with open(temp_audio_path, "wb") as f:
        f.write(audio_file.read())

    # Transcribe audio using Azure STT
    transcribed_text = azure_stt(temp_audio_path)
    if transcribed_text:
        st.session_state['question'] = transcribed_text  # Store the transcribed question
    else:
        st.session_state['question'] = "Sorry, I couldn't process your audio."

    # Process the question and generate response
    response = get_response(st.session_state['question'])
    st.session_state['response'] = response["answer"]

    # Generate TTS response if in voice mode
    if st.session_state['is_voice']:
        st.session_state['audio_response'] = azure_tts(st.session_state['response'])

# Function to interact with the QA chain
def get_response(question):
    if "hunar" not in question:
        question += " hunar"
    ans = chain.invoke({"input": question})
    return ans

# Streamlit frontend
st.title("The Hunar Foundation Bot")
st.sidebar.title("Toggle Chat Mode")
chat_mode = st.sidebar.radio("Select Chat Mode", ("Text Chat", "Voice Chat"))

# Text Chat Mode
if chat_mode == "Text Chat":
    st.session_state['is_voice'] = False
    question = st.text_input("Ask a question:")

    if question:
        response = get_response(question)
        st.write(response["answer"])

# Voice Chat Mode
else:
    st.session_state['is_voice'] = True

    # Display audio input widget for voice recording
    audio_file = st.audio_input("Record your question")

    if audio_file:
        process_audio_input(audio_file)

    # Display transcribed text and TTS response
    if st.session_state.get('question'):
        st.write(f"Your Question: {st.session_state['question']}")

    # Play audio response using st.audio
    if st.session_state.get('audio_response'):
        st.audio(st.session_state['audio_response'], format="audio/mp3", autoplay=True)
