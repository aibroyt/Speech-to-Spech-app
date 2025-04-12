import streamlit as st
  import torchaudio
  from bark import generate_audio, SAMPLE_RATE
  from scipy.io.wavfile import write

  st.set_page_config(page_title="Speech to Speech AI", layout="centered")
  st.title("Speech to Speech Generator (Multi Voice)")

  voices = {
      "Narrator (English)": "v2/en_speaker_9",
      "Young Female": "v2/en_speaker_6",
      "Young Male": "v2/en_speaker_5",
      "Elderly Male": "v2/en_speaker_1",
      "Elderly Female": "v2/en_speaker_3"
  }

  text_input = st.text_area("Enter your script:", "Welcome to your AI generated voice-over!")
  selected_voice = st.selectbox("Choose a voice:", list(voices.keys()))

  if st.button("Generate Voice"):
      with st.spinner("Generating audio..."):
          audio_array = generate_audio(text_input, history_prompt=voices[selected_voice])
          output_path = "generated_voice.wav"
          write(output_path, SAMPLE_RATE, audio_array)
          st.success("Done!")
          st.audio(output_path)
          with open(output_path, "rb") as f:
              st.download_button("Download Audio", f, file_name="voice_output.wav")
