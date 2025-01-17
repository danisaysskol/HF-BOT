import streamlit as st
import whisper
import sounddevice as sd
import numpy as np
import tempfile
import os
import wave
import pygame
from gtts import gTTS
from helper import get_QA_chain

# Load the Whisper model
model = whisper.load_model("base")

# Initialize the Q&A chain
chain = get_QA_chain()

def get_response(question):
    chain = get_QA_chain()
    ans = chain.invoke({"input": question})
    return ans

# Function to record audio using sounddevice
def record_audio(duration=5, fs=16000):
    """ Record audio and return the audio data and file path """
    st.info("Recording... Speak now.")
    
    # Record audio
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until the recording is finished
    
    # Save to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as f:
        with wave.open(f, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 2 bytes for int16
            wf.setframerate(fs)
            wf.writeframes(recording.tobytes())
            audio_file_path = f.name

    st.info("Recording complete.")
    return audio_file_path

# Function to transcribe audio using Whisper
def transcribe_audio(audio_file_path):
    result = model.transcribe(audio_file_path)
    return result['text']

# Function to speak the response using gTTS
def speak_response(response_text):
    """ Generate speech from text and play it using gTTS and pygame """
    # Generate speech using Google Text-to-Speech
    tts = gTTS(text=response_text, lang='en')
    
    # Save the speech to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
        tts.save(f.name)
        audio_file_path = f.name

    # Initialize pygame mixer to play the audio
    pygame.mixer.init()

    # Load and play the audio
    pygame.mixer.music.load(audio_file_path)
    pygame.mixer.music.play()

    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():  # Wait until the music finishes playing
        pygame.time.Clock().tick(10)

    # Clean up the audio file after playing
    os.remove(audio_file_path)

# Streamlit app UI
st.title("The Hunar Foundation Chatbot Q&A 🌱")

# Select mode: Text input or Voice input
mode = st.radio("Choose input mode:", ("Text", "Voice"))

if mode == "Text":
    # Text-based input remains unchanged
    question = st.text_input("Question: ")

    if question:
        print(question)
        response = get_response(question)
        st.header("Answer")
        st.write(response["answer"])
        print(response['answer'])

elif mode == "Voice":
    # Buttons to start and stop the recording
    record_button = st.button("Start Recording")
    stop_button = st.button("Stop Recording")

    # Start recording on button click
    if record_button:
        # Record the audio and get the file path
        audio_file_path = record_audio(duration=5)  # 5 seconds by default
        st.info(f"Audio recorded and saved at: {audio_file_path}")

        # Transcribe the recorded audio
        transcription = transcribe_audio(audio_file_path)

        st.header("You asked:")
        st.write(transcription)

        # Get the chatbot's response
        response = get_response(transcription)

        st.header("Answer:")
        st.write(response["answer"])

        # Save the response for later playback when the user clicks "Listen"
        st.session_state.response_text = response["answer"]
        st.session_state.audio_ready = True  # Flag to indicate the response is ready to be spoken

        # Clean up by deleting the temporary audio file
        os.remove(audio_file_path)

    # Stop recording manually
    if stop_button:
        st.info("Recording stopped by user.")
        sd.stop()  # Stop the audio recording immediately

    # Add a "Listen" button to play the response when the user is ready
    if "audio_ready" in st.session_state and st.session_state.audio_ready:
        listen_button = st.button("Listen")
        
        if listen_button:
            speak_response(st.session_state.response_text)
            st.session_state.audio_ready = False  # Reset the flag after playing the audio
