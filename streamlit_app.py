import streamlit as st
import requests

# FastAPI endpoint
API_URL = "http://127.0.0.1:8000/api/v1"

st.set_page_config(page_title="College AI System", layout="wide")

st.title("📚 College AI System")
st.markdown("---")

# -------------------------------
# SIDEBAR
# -------------------------------

mode = st.sidebar.selectbox(
    "Select Mode",
    [
        "Student Data Q&A",
        "PDF Chat",
        "Excel/CSV Chat"
    ]
)

model_option = st.sidebar.selectbox(
    "Select Model",
    [
        "qwen2.5:7b",
        "llama3.1:8b",
        "qwen2.5:1.5b",
        "qwen2.5-coder:3b"
    ]
)

# -------------------------------
# STUDENT DATA MODE
# -------------------------------

if mode == "Student Data Q&A":

    st.header("🎓 Ask Questions About Student Data")

    user_input = st.text_input("Enter your question")

    if st.button("Ask") and user_input:

        payload = {
            "question": user_input,
            "model": model_option
        }

        response = requests.post(
            f"{API_URL}/ask",
            json=payload
        )

        if response.status_code == 200:
            data = response.json()
            st.success(data["response"])
        else:
            st.error("Error connecting to backend")


# -------------------------------
# PDF CHAT MODE
# -------------------------------

elif mode == "PDF Chat":

    st.header("📄 Upload PDF and Ask Questions")

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if uploaded_file:

        with st.spinner("Uploading and processing PDF..."):
            response = requests.post(
                f"{API_URL}/files/upload",
                files={"file": uploaded_file}
            )

        if response.status_code == 200:
            st.success("PDF uploaded successfully!")

            question = st.text_input("Ask a question about the PDF")

            if st.button("Ask PDF") and question:

                payload = {
                    "question": question,
                    "model": model_option
                }

                response = requests.post(
                    f"{API_URL}/files/ask",
                    json=payload
                )

                if response.status_code == 200:
                    data = response.json()
                    st.success(data["response"])
                else:
                    st.error("Error asking PDF question")


        else:
            st.error("Upload failed")


# -------------------------------
# EXCEL / CSV MODE
# -------------------------------

elif mode == "Excel/CSV Chat":

    st.header("📊 Upload Excel or CSV and Ask Questions")

    uploaded_file = st.file_uploader(
        "Upload Excel or CSV",
        type=["xlsx", "xls", "csv"]
    )

    if uploaded_file:

        with st.spinner("Uploading and processing file..."):
            response = requests.post(
                f"{API_URL}/files/upload",
                files={"file": uploaded_file}
            )

        if response.status_code == 200:
            st.success("File uploaded successfully!")

            question = st.text_input("Ask a question about the data")

            if st.button("Ask Data") and question:

                payload = {
                    "question": question,
                    "model": model_option
                }

                response = requests.post(
                    f"{API_URL}/files/ask",
                    json=payload
                )

                if response.status_code == 200:
                    data = response.json()
                    st.success(data["response"])
                else:
                    st.error("Error asking data question")

        else:
            st.error("Upload failed")