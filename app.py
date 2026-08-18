import streamlit as st
from deep_translator import GoogleTranslator
import io
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr

# Page configuration
st.set_page_config(
    page_title="AI Language Translator",
    page_icon="🌐",
    layout="centered"
)
st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 20%, rgba(90, 70, 180, 0.25), transparent 35%),
        radial-gradient(circle at 90% 80%, rgba(0, 180, 200, 0.20), transparent 35%),
        linear-gradient(135deg, #080b18, #11152b, #090d1c);
    color: white;
}

/* Main title */
h1 {
    text-align: center;
    font-weight: 700;
    letter-spacing: 1px;
}

/* Subtitle */
.stMarkdown p {
    text-align: center;
}

/* Input boxes */
textarea {
    background-color: rgba(255, 255, 255, 0.08) !important;
    color: white !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 15px !important;
}

 Buttons 
.stButton > button {
    width: 100%;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.15);
    background: rgba(255,255,255,0.08);
    color: white;
    font-weight: 600;
    transition: 0.3s;
}

.stButton > button:hover {
    background: rgba(100, 120, 255, 0.25);
    border-color: rgba(150, 160, 255, 0.5);
}

/* Select boxes */
div[data-baseweb="select"] > div {
    background-color: rgba(255,255,255,0.08);
    border-radius: 12px;
}

</style>
""",unsafe_allow_html=True)
# Title
st.title("🌐 AI Language Translation Tool")
st.write("Translate text between different languages instantly.")

# Supported languages
languages = {
    "English": "en",
    "Hindi": "hi",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Japanese": "ja",
    "Chinese": "zh-CN"
}

# Swap languages
if "source_language" not in st.session_state:
    st.session_state.source_language = "English"

if "target_language" not in st.session_state:
    st.session_state.target_language = "Hindi"

def swap_languages():
    source = st.session_state.source_language
    target = st.session_state.target_language

    st.session_state.source_language = target
    st.session_state.target_language = source
# Language selection
col1, col2 = st.columns(2)

with col1:
    source_language = st.selectbox(
        "Source Language",
        list(languages.keys()),
        key="source_language"
    )

with col2:
    target_language = st.selectbox(
        "Target Language",
        list(languages.keys()),
        key="target_language"
    )

    st.button(
    "🔄 Swap Languages",
    on_click=swap_languages,
    use_container_width=True
)
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

    # Speech-to-text
st.subheader("🎤 Speak your text")

audio = audio_recorder(
    text="Click to record",
    recording_color="#FF4B4B",
    neutral_color="#6E6E6E",
  
)

if audio:
    recognizer = sr.Recognizer()

    audio_bytes = io.BytesIO(audio)

    with sr.AudioFile(audio_bytes) as source:
        recorded_audio = recognizer.record(source)

    try:
        spoken_text = recognizer.recognize_google(
            recorded_audio,
            language=languages[source_language]
        )

        st.session_state.input_text = spoken_text
        st.success("Speech converted to text successfully!")

    except sr.UnknownValueError:
        st.warning("Sorry, I could not understand your speech.")

    except sr.RequestError:
        st.error("Speech recognition service is unavailable. Please check your internet connection.")
# Text input
text = st.text_area(
    "Enter text to translate:",
    height=150,
    placeholder="Type your text here...",
    key="input_text"
)

# Translate button
if st.button("Translate 🚀", use_container_width=True):

    if not text.strip():
        st.warning("Please enter some text first.")

    elif source_language == target_language:
        st.info("Source and target languages are the same.")

    else:
        try:
            translator = GoogleTranslator(
                source=languages[source_language],
                target=languages[target_language]
            )

            translated_text = translator.translate(text)

            st.subheader("Translation")
            st.success(translated_text)

           

        except Exception as e:
            st.error("Translation failed. Please check your internet connection and try again.")