import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig, SpeechSynthesizer

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

# Azure Keys and Region
STT_KEY = os.getenv("AZURE_STT_KEY")  # Replace with your Speech-to-Text Azure key
STT_REGION = os.getenv("AZURE_STT_REGION")  # Replace with your Speech-to-Text Azure region
TTS_KEY = os.getenv("AZURE_TTS_KEY")  # Replace with your Text-to-Speech Azure key
TTS_REGION = os.getenv("AZURE_TTS_REGION")  # Replace with your Text-to-Speech Azure region

def azure_stt(audio_file):
    """
    Convert speech to text using Azure Speech SDK.
    Args:
        audio_file (BytesIO): The audio file in WAV or MP3 format.
    Returns:
        str: Transcribed text from the audio.
    """
    # Set up Azure STT configuration
    speech_config = SpeechConfig(subscription=STT_KEY, region=STT_REGION)
    audio_config = AudioConfig(filename=audio_file.name)  # Use filename for uploaded file

    # Recognizer
    recognizer = SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    
    print("Recognizing speech...")
    result = recognizer.recognize_once()

    # Handle STT result
    if result.reason == result.Reason.RecognizedSpeech:
        return result.text
    elif result.reason == result.Reason.NoMatch:
        return "Sorry, I couldn't understand the audio. Please try again."
    else:
        raise Exception(f"Speech recognition failed: {result.reason}")

def azure_tts(text):
    """
    Convert text to speech using Azure Speech SDK.
    Args:
        text (str): Text to be converted into speech.
    Returns:
        BytesIO: Audio content in WAV format.
    """
    # Set up Azure TTS configuration
    speech_config = SpeechConfig(subscription=TTS_KEY, region=TTS_REGION)
    speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"  # Choose a suitable voice

    # Synthesizer
    synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    print("Generating speech...")
    result = synthesizer.speak_text_async(text).get()

    # Handle TTS result
    if result.reason == result.Reason.SynthesizingAudioCompleted:
        return result.audio_data
    else:
        raise Exception(f"Speech synthesis failed: {result.reason}")
