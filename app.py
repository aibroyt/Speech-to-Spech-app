import streamlit as st
import speech_recognition as sr
from TTS.api import TTS
import tempfile
import os
from pydub import AudioSegment
import base64

st.set_page_config(page_title="Speech-to-Speech App", layout="centered")
st.title("Speech-to-Speech AI Tool")

uploaded_audio = st.file_uploader("Upload a voice file (wav/mp3)", type=["wav", "mp3"])

if uploaded_audio:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
        if uploaded_audio.type == "audio/mpeg":
            sound = AudioSegment.from_mp3(uploaded_audio)
            sound.export(tmp_audio.name, format="wav")
        else:
            tmp_audio.write(uploaded_audio.read())
        temp_audio_path = tmp_audio.name

    recognizer = sr.Recognizer()
    with sr.AudioFile(temp_audio_path) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            st.success("Transcribed text: " + text)
        except sr.UnknownValueError:
            st.error("Could not understand audio.")
        except sr.RequestError as e:
            st.error(f"Could not request results; {e}")

    selected_voice = st.selectbox("Choose a voice style", ["random", "female-en-1", "male-en-2"])

    if st.button("Generate Voice"):
        tts = TTS(model_name="tts_models/en/vctk/vits", progress_bar=False)
        out_path = os.path.join(tempfile.gettempdir(), "output.wav")
        tts.tts_to_file(text=text, speaker=selected_voice, file_path=out_path)

        audio_bytes = open(out_path, 'rb').read()
        st.audio(audio_bytes, format='audio/wav')

        b64 = base64.b64encode(audio_bytes).decode()
        href = f'<a href="data:audio/wav;base64,{b64}" download="output.wav">Download output</a>'
        st.markdown(href, unsafe_allow_html=True)
