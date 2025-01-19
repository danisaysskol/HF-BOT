import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
from io import BytesIO

# Load environment variables from a .env file
load_dotenv()

# Retrieve Azure Speech API credentials from environment variables
STT_KEY = os.getenv("AZURE_STT_KEY")
STT_REGION = os.getenv("AZURE_STT_REGION")

# Validate environment variables
if not STT_KEY or not STT_REGION:
    raise ValueError("Azure STT API Key or Region is not set properly in the environment variables.")

def azure_stt(audio_file_path):
    """
    Converts audio from a file to text using Azure's Speech-to-Text service.
    """
    # Configure Azure Speech settings
    speech_config = speechsdk.SpeechConfig(subscription=STT_KEY, region=STT_REGION)
    audio_config = speechsdk.audio.AudioConfig(filename=audio_file_path)

    # Initialize speech recognizer
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # Perform speech recognition
    result = recognizer.recognize_once()

    # Handle recognition results
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return "Sorry, no speech could be recognized."
    else:
        return f"Error: {result.error_details}"

def azure_tts(text):
    """
    Converts text to speech using Azure's Text-to-Speech service and returns the audio data.
    """
    # Configure Azure Speech settings
    speech_config = speechsdk.SpeechConfig(subscription=STT_KEY, region=STT_REGION)
    speech_config.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3
    )

    # Specify the output audio file
    output_file = "output_audio.mp3"
    audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)

    # Initialize the synthesizer
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    # Perform the text-to-speech synthesis
    result = synthesizer.speak_text_async(text).get()

    # Handle the result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        # Read the audio data from the file
        with open(output_file, "rb") as audio_file:
            audio_data = audio_file.read()
        return audio_data
    else:
        raise RuntimeError(f"TTS failed: {result.error_details}")
