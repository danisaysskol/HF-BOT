import streamlit as st
import whisper
from pydub import AudioSegment
import io

# Initialize Whisper model
@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()

# Streamlit app title
st.title("Whisper Transcription App")

# Audio recorder
audio_input = st.audio_input("Record your message")

if audio_input is not None:
    # Convert the audio data to a format compatible with Whisper
    audio_bytes = audio_input.getvalue()
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format="wav")
    audio.export("temp_audio.wav", format="wav")

    # Transcribe audio
    st.info("Transcribing audio...")
    result = model.transcribe("temp_audio.wav")
    st.success("Transcription completed!")

    # Display transcription
    st.header("Transcription")
    st.write(result["text"])

    # Provide download option
    st.download_button("Download Transcription", result["text"], file_name="transcription.txt")
