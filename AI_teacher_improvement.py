import streamlit as st
import google.generativeai as genai
import speech_recognition as sr
from gtts import gTTS
import os
import tempfile

# ✅ Google Gemini API Key
GOOGLE_API_KEY = "AIzaSyBv1OdaOSIY83PKobrEJNPmTUVdY4iqsiU"
genai.configure(api_key=GOOGLE_API_KEY)

# ✅ Streamlit UI Setup
st.set_page_config(page_title="📚 AI Teacher", layout="wide")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("📚 AI Teacher Assistant (Gemini AI)")

# ✅ Language Selection
language = st.selectbox("Select Medium of Instruction:", ["English", "Marathi", "Bhojpuri","Hindi"], index=0)

# ✅ Function to Call Gemini API
def get_response(question, lang):
    optimized_prompt = f"""
    You are an AI teacher for primary school students in Maharashtra, India.
    - Give a short, simple, and **to-the-point** answer (max 3 sentences).
    - Always explain where this subject is used in **real life or careers**.
    - If the student asks about practical use, mention **one profession** that uses it.
    - Answer in {lang} language.
    
    Question: {question}
    Answer:
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(optimized_prompt)
        answer = response.text if response else "Error: Unable to fetch response from Gemini."
    except Exception as e:
        answer = f"Error: {str(e)}"
    
    st.session_state.chat_history.append((question, answer))
    return answer

# ✅ Function to Recognize Speech
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak now!")
        try:
            audio = recognizer.listen(source, timeout=5)
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Could not understand audio. Please try again."
        except sr.RequestError:
            return "Speech recognition service unavailable."

# ✅ Function to Read AI Response Using gTTS
def speak_response(response, lang):
    lang_code = {"English": "en", "Marathi": "mr", "Hindi": "hi"}.get(lang, "en")
    tts = gTTS(text=response, lang=lang_code, slow=False)
    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as fp:
        tts.save(fp.name)
        os.system(f"mpg321 {fp.name} -q")

# ✅ Chat Interface
st.subheader("Chat with AI Teacher")

col1, col2 = st.columns([3, 1])
with col1:
    question = st.text_input("Ask your question:")
with col2:
    if st.button("🎙️ Speak"):
        question = recognize_speech()
        st.text_input("Recognized Speech:", value=question, key="speech_input", disabled=True)

if st.button("Send", use_container_width=True):
    if question:
        with st.spinner("Thinking..."):
            response = get_response(question, language)
        st.success("AI Teacher's Response:")
        st.write(response)
        speak_response(response, language)  # AI reads answer aloud
    else:
        st.warning("Please enter a question.")

# ✅ Display Chat History
st.subheader("Conversation History")
for q, a in st.session_state.chat_history[-5:]:  # Show last 5 exchanges
    st.write(f"**You:** {q}")
    st.write(f"**AI Teacher:** {a}")
    st.write("---")
