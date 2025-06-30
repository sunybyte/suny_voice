import streamlit as st
import requests

# Load secrets
API_KEY = st.secrets["API_KEY"]
VOICE_ID = st.secrets["VOICE_ID"]

# Streamlit UI
st.set_page_config(page_title="AI Voice Generator")
st.title("🔊 Text to Speech Generator")

text_input = st.text_area("Enter your text:")

if st.button("Convert to Speech"):
    if not text_input.strip():
        st.warning("Please enter some text.")
    else:
        with st.spinner("Generating voice..."):

            url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

            headers = {
                "accept": "audio/mpeg",
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

            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 200:
                # Save audio to file
                with open("output.mp3", "wb") as f:
                    f.write(response.content)

                st.success("✅ Voice generated successfully!")
                st.audio("output.mp3")
            else:
                st.error(f"❌ Error {response.status_code}: Could not generate voice.")
                st.text("Details:\n" + response.text)
