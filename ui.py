import streamlit as st
from response_handler import get_response
from speech_handler import get_audio_input, text_to_speech

def render_ui():
    """Render the Streamlit UI elements for the chatbot."""
    
    # Initialize session state variables
    for key in ['last_response', 'last_question', 'is_listening']:
        if key not in st.session_state:
            st.session_state[key] = None if key != 'is_listening' else False

    # Input mode selection
    input_mode = st.radio("Choose your input method:", ("Text", "Voice"))

    if input_mode == "Text":
        # Text Input Section
        question_text = st.text_input("Enter your question:")
        if question_text:
            st.session_state.last_question = question_text
            response = get_response(question_text)
            if response:
                st.session_state.last_response = response["answer"]
                st.header("Answer")
                st.write(response["answer"])

                # Unified "Listen" Button
                if st.button("Listen" if not st.session_state.is_listening else "Stop Listening"):
                    st.session_state.is_listening = not st.session_state.is_listening
                    if st.session_state.is_listening:
                        text_to_speech(st.session_state.last_response)

    elif input_mode == "Voice":
        # Voice Input Section
        if st.button("Start Voice Input"):
            st.session_state.last_question = get_audio_input()

            if st.session_state.last_question:
                st.write(f"Processing your voice input... Transcribed: {st.session_state.last_question}")
                response = get_response(st.session_state.last_question)
                if response:
                    st.session_state.last_response = response["answer"]
                    st.header("Answer")
                    st.write(response["answer"])

                    # Unified "Listen" Button
                    if st.button("Listen" if not st.session_state.is_listening else "Stop Listening"):
                        st.session_state.is_listening = not st.session_state.is_listening
                        if st.session_state.is_listening:
                            text_to_speech(st.session_state.last_response)
