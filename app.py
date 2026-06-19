import streamlit as st
from deep_translator import GoogleTranslator
from langdetect import detect
from gtts import gTTS
import pyperclip
import os

def load_css():
    with open("style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()
st.set_page_config(
    page_title="AI Language Translator",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 AI Language Translation Tool")
st.write("Translate text between multiple languages")

languages = {
    "English": "en",
    "Tamil": "ta",
    "Hindi": "hi",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Japanese": "ja",
    "Chinese": "zh-CN"
}

if "history" not in st.session_state:
    st.session_state.history = []

text = st.text_area(
    "Enter Text",
    height=150
)

st.write(f"Character Count: {len(text)}")

col1, col2 = st.columns(2)

with col1:
    source = st.selectbox(
        "Source Language",
        list(languages.keys())
    )

with col2:
    target = st.selectbox(
        "Target Language",
        list(languages.keys())
    )

if st.button("Translate"):

    if text:

        try:

            detected = detect(text)

            translated = GoogleTranslator(
                source=languages[source],
                target=languages[target]
            ).translate(text)

            st.subheader("Translated Text")

            st.success(translated)

            st.write(f"Detected Language Code: {detected}")

            st.session_state.history.append(
                {
                    "Original": text,
                    "Translated": translated
                }
            )

            tts = gTTS(
                translated,
                lang=languages[target]
            )

            tts.save("translated.mp3")

            audio_file = open(
                "translated.mp3",
                "rb"
            )

            st.audio(audio_file.read())

            st.download_button(
                "Download Translation",
                translated,
                file_name="translation.txt"
            )

        except Exception as e:
            st.error(e)

copy_text = st.text_input(
    "Copy Translation Here"
)

if st.button("Copy Text"):
    pyperclip.copy(copy_text)
    st.success("Copied Successfully!")

if st.button("Clear"):
    st.rerun()

st.subheader("Translation History")

for item in st.session_state.history[::-1]:

    st.write("Original:")
    st.info(item["Original"])

    st.write("Translated:")
    st.success(item["Translated"])

    st.divider()
