import streamlit as st
import requests

# FastAPI endpoint
API_URL = "http://127.0.0.1:8000/api/v1/ask"

st.set_page_config(page_title="School System AI", layout="centered")

st.title("🎓 School System AI Chatbot")

# --- Input Row (Question + Model + Button) ---
col1, col2, col3 = st.columns([5, 2, 1])

with col1:
    question = st.text_input(
        "Ask your question:",
        label_visibility="collapsed",
        placeholder="Ask your question..."
    )

with col2:
    model_option = st.selectbox(
        "Model",
        [
        "llama3.1:8b",
        "qwen2.5:1.5b",
        "qwen2.5-coder:3b"
        ],

        label_visibility="collapsed"
    )

with col3:
    submit = st.button("Ask")

# --- When Ask is clicked ---
if submit:

    if question.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner(f"Running on {model_option.upper()} model..."):

            try:
                response = requests.post(
                    API_URL,
                    json={
                        "question": question,
                        "model": model_option   
                    }
                )

                if response.status_code == 200:
                    data = response.json()

                    st.success("Response received ✅")

                    st.write("### 💬 Answer:")
                    st.write(data.get("response"))

                    # Show structured query only if exists
                    if data.get("structured_query"):
                        st.write("### 📊 Structured Query:")
                        st.json(data.get("structured_query"))

                else:
                    st.error(f"API Error: {response.status_code}")
                    st.text(response.text)

            except Exception as e:
                st.error(f"Error connecting to API: {e}")
