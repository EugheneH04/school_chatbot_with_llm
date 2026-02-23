import streamlit as st
import requests

# FastAPI endpoint
API_URL = "http://127.0.0.1:8000/api/v1/ask"

st.set_page_config(page_title="School System AI", layout="centered")

st.title("School System AI Chatbot")

# User input
question = st.text_input("Ask your question:")

if st.button("Submit"):

    if question.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):

            try:
                response = requests.post(
                    API_URL,
                    json={"question": question}
                )

                if response.status_code == 200:
                    data = response.json()

                    st.success("Response received ✅")

                    st.write("### 📊 Result:")
                    st.write(data.get("response"))

                    st.write("### 📌 Structured Query:")
                    st.json(data.get("structured_query"))

                else:
                    st.error(f"API Error: {response.status_code}")
                    st.text(response.text)

            except Exception as e:
                st.error(f"Error connecting to API: {e}")
