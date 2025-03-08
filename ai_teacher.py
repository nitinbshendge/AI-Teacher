import streamlit as st
import ollama

# ✅ Optimize Streamlit UI
st.set_page_config(page_title="📚 AI Teacher", layout="wide")

if "responses" not in st.session_state:
    st.session_state.responses = {}

st.title("📚 AI Teacher Assistant")

# ✅ Optimized Function for Faster Response
def get_response(question):
    if question in st.session_state.responses:
        return st.session_state.responses[question]
    
    optimized_prompt = f"""
    You are an AI teacher for primary school students in Maharashtra, India.
    - Give a short, simple, and **to-the-point** answer (max 3 sentences).
    - Always explain where this subject is used in **real life or careers**.
    - If the student asks about practical use, mention **one profession** that uses it.

    Question: {question}
    Answer:
    """
    
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": optimized_prompt}])
    answer = response["message"]["content"]
    
    # ✅ Cache answer to avoid re-processing
    st.session_state.responses[question] = answer
    return answer

# ✅ User Input Section
question = st.text_input("Ask your question:")

if st.button("Get Answer", use_container_width=True):
    if question:
        with st.spinner("Thinking..."):
            response = get_response(question)
        st.success("Here's your answer:")
        st.write(response)
    else:
        st.warning("Please enter a question.")
