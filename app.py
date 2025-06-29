import streamlit as st
import requests

# Load secrets (You must set these in Streamlit Cloud > Settings > Secrets)
API_KEY = st.secrets["API_KEY"]
VOICE_ID = st.secrets["VOICE_ID"]

# Streamlit UI
st.set_page_config(page_title="Text to Speech AI", layout="centered")
st.title("🔊 AI Voice Generator")
text_input = st.text_area("Enter text to convert into speech:")

if st.button("Convert to Speech"):
    if not text_input.strip():
        st.warning("Please enter some text first.")
    else:
        with st.spinner("Generating speech..."):

            # Make API request to ElevenLabs
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
            headers = {
                "xi-api-key": API_KEY,
                "Content-Type": "application/json"
            }
            data = {
                "text": text_input,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75
                }
            }

            response = requests.post(url, json=data, headers=headers)

            if response.status_code == 200:
                # Save audio to file
                audio_file_path = "output.mp3"
                with open(audio_file_path, "wb") as f:
                    f.write(response.content)

                st.success("✅ Voice created successfully!")
                st.audio(audio_file_path)
            else:
                st.error(f"Failed to generate voice. Status code: {response.status_code}")
