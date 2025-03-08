import streamlit as st
import requests
import json

# ✅ Groq API Key (Replace with your own API key)
GROQ_API_KEY = "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"
GROQ_MODEL = "mistral-7b-8192"  # Using a lighter model for performance
print("API Key:", GROQ_API_KEY)

# ✅ Streamlit UI Setup
st.set_page_config(page_title="📚 AI Teacher", layout="wide")

if "responses" not in st.session_state:
    st.session_state.responses = {}

st.title("📚 AI Teacher Assistant (Groq AI)")

# ✅ Language Selection
language = st.selectbox("Select Medium of Instruction:", ["English", "Marathi", "Hindi"], index=0)

# ✅ Function to Call Groq API
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

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": optimized_prompt}],
        "temperature": 0.5,
    }

    try:
        response = requests.post("https://api.groq.com/v1/chat/completions", headers=headers, data=json.dumps(data))
        response_json = response.json()

        if "choices" in response_json:
            answer = response_json["choices"][0]["message"]["content"]
        else:
            answer = "Error: Unable to fetch response from Groq. Please check API key and model."
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
