import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Retrieve Azure Speech API credentials from environment variables
STT_KEY = os.getenv("AZURE_STT_KEY")
STT_REGION = os.getenv("AZURE_STT_REGION")

# Validate environment variables
if not STT_KEY or not STT_REGION:
    raise ValueError("Azure STT API Key or Region is not set properly in the environment variables.")

def azure_stt():
    """
    Captures audio from the default microphone and converts it to text using Azure's Speech-to-Text service.
    """
    # Configure speech settings for Speech-to-Text
    speech_config = speechsdk.SpeechConfig(subscription=STT_KEY, region=STT_REGION)
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

    # Initialize the recognizer
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Please speak your question.")

    # Perform speech recognition
    result = recognizer.recognize_once()

    # Handle recognition result
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"Recognized: {result.text}")
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized.")
        return "Sorry, I couldn't hear your question. Please try again."
    else:
        print(f"Speech recognition failed: {result.error_details}")
        return "There was an error processing your speech."



def azure_tts(text):
    """
    Converts the provided text to speech using Azure's Text-to-Speech service and plays it through the default speaker.
    """
    # Configure speech settings for Text-to-Speech
    speech_config = speechsdk.SpeechConfig(subscription=STT_KEY, region=STT_REGION)

    # Create audio output configuration for the default speaker
    audio_output_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    # Initialize the synthesizer with the speech and audio configurations
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output_config)

    # Perform text-to-speech synthesis
    synthesizer.speak_text_async(text)

    print(f"Speaking: {text}")


