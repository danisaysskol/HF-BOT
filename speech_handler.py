import os
import azure.cognitiveservices.speech as speechsdk
import streamlit as st
from whisper_stt import whisper_stt

def text_to_speech(text):
    """Convert text to speech using Azure TTS."""
    try:
        speech_key = os.getenv("AZURE_SPEECH_KEY")
        speech_region = os.getenv("AZURE_SPEECH_REGION")

        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
        speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"

        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        result = synthesizer.speak_text_async(text).get()

        if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
            raise Exception(f"Speech synthesis error: {result.cancellation_details.reason}")
    except Exception as e:
        st.error("An error occurred while generating audio.")
        print(f"TTS Error: {e}")

def get_audio_input():
    """Capture and transcribe audio input."""
    try:
        audio = whisper_stt(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            language="en",
            key="voice_input"
        )
        return audio
    except Exception as e:
        st.error("An error occurred while processing your audio input.")
        print(f"STT Error: {e}")
        return None
