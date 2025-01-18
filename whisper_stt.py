from streamlit_mic_recorder import mic_recorder
import streamlit as st
import io
import os
import openai

def whisper_stt(openai_api_key=None, language=None, key=None):
    """Capture audio using the mic recorder and transcribe it using OpenAI's Whisper."""
    audio = mic_recorder(start_prompt="Start recording", stop_prompt="Stop recording", format="webm", key=key)

    if not audio:
        return None

    try:
        openai.api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        audio_file = io.BytesIO(audio['bytes'])
        audio_file.name = 'audio.webm'

        response = openai.Audio.transcribe("whisper-1", audio_file, language=language)
        return response.get("text")
    except Exception as e:
        st.error("Failed to process the audio input.")
        print(f"Whisper STT Error: {e}")
        return None
