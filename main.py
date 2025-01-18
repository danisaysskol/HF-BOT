import streamlit as st
from streamlit_mic_recorder import mic_recorder
from whisper_stt import whisper_stt
from helper import get_QA_chain
import os
import azure.cognitiveservices.speech as speechsdk
# import requests
# from io import BytesIO
# import tempfile


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


import azure.cognitiveservices.speech as speechsdk

def text_to_speech(text):
    """Convert text to speech using Azure TTS and play the audio."""
    try:
        # Fetch Azure credentials from environment variables
        speech_key = os.getenv("AZURE_SPEECH_KEY")  # Replace with your Azure Speech Key
        speech_region = os.getenv("AZURE_SPEECH_REGION")  # Replace with your Azure Region

        # Initialize the Speech SDK
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

        # Set the voice and language
        speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"  # Change voice as needed

        # Create a synthesizer
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

        # Generate speech
        result = synthesizer.speak_text_async(text).get()

        # Check result status
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized successfully.")
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            raise Exception(f"Speech synthesis canceled: {cancellation_details.reason}")
    except Exception as e:
        st.error("An error occurred while generating audio.")
        print(f"TTS Error: {e}")

def main():
    st.title("The Hunar Foundation Chatbot Q&A 🌱")

    # State initialization
    if 'last_response' not in st.session_state:
        st.session_state.last_response = None
    if 'last_question' not in st.session_state:
        st.session_state.last_question = None

    # Text Input Section
    question = st.text_input("Ask a question (Text Mode):")
    if question:
        st.session_state.last_response = None
        st.session_state.last_question = question
        response = get_response(question)
        if response:
            st.session_state.last_response = response["answer"]
            st.header("Answer")
            st.write(response["answer"])

    # Voice Input Section
    st.write("### Or ask a question using your voice:")
    audio = whisper_stt(
        openai_api_key=os.getenv("OPENAI_API_KEY"),  # Load API key from .env
        language="en",
        start_prompt="Start Recording",
        stop_prompt="Stop Recording",
        just_once=True,
        key="voice_input"
    )

    if audio:
        st.session_state.last_response = None
        st.session_state.last_question = audio
        st.write("Processing your voice input...")
        response = get_response(audio)
        if response:
            st.session_state.last_response = response["answer"]
            st.header("Answer")
            st.write(response["answer"])

    # Listen to Response Section
    if st.session_state.last_response:
        if st.button("Listen to Response"):
            text_to_speech(st.session_state.last_response)


# Run the main function
if __name__ == "__main__":
    main()
    