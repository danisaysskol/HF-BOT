import streamlit as st
from response_handler import get_response
from speech_handler import text_to_speech, get_audio_input
from ui import render_ui

def main():
    st.title("The Hunar Foundation Chatbot Q&A 🌱")
    
    # Rendering the UI
    render_ui()

# Run the main function
if __name__ == "__main__":
    main()
