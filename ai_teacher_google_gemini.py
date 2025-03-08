import streamlit as st
import google.generativeai as genai

# ✅ Google Gemini API Key (Replace with your own API key)
GOOGLE_API_KEY = "AIzaSyBv1OdaOSIY83PKobrEJNPmTUVdY4iqsiU"
genai.configure(api_key=GOOGLE_API_KEY)

# ✅ Streamlit UI Setup
st.set_page_config(page_title="📚 AI Teacher", layout="wide")

if "responses" not in st.session_state:
    st.session_state.responses = {}

st.title("📚 AI Teacher Assistant (Gemini AI)")

# ✅ Language Selection
language = st.selectbox("Select Medium of Instruction:", ["English", "Marathi", "Hindi"], index=0)

# ✅ Function to Call Gemini API
def get_response(question, lang):
    if (question, lang) in st.session_state.responses:
        return st.session_state.responses[(question, lang)]

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
         
        model = genai.GenerativeModel("gemini-1.5-flash")  # Use what you found in the list

        response = model.generate_content(optimized_prompt)
        answer = response.text if response else "Error: Unable to fetch response from Gemini."
    except Exception as e:
        answer = f"Error: {str(e)}"

    st.session_state.responses[(question, lang)] = answer
    return answer

# ✅ User Input Section
question = st.text_input("Ask your question:")

if st.button("Get Answer", use_container_width=True):
    if question:
        with st.spinner("Thinking..."):
            response = get_response(question, language)
        st.success("Here's your answer:")
        st.write(response)
    else:
        st.warning("Please enter a question.")
