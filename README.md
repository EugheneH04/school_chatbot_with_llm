# school_chatbot_with_llm

AI-powered School Management Chatbot built using FastAPI and Local LLM (Ollama).

---

## 🚀 Overview

This project is a backend chatbot system designed for school data interaction and document-based question answering.

It integrates:
- FastAPI for backend API
- Ollama for running local LLMs
- RAG (Retrieval Augmented Generation) for PDF question answering
- Structured query execution for student-related data queries

---

## 🧠 Features

- FastAPI REST API
- Local LLM integration (Llama / Qwen models)
- Multi-model selection support
- PDF upload and question answering (RAG)
- Structured student data queries
- Modular service-based architecture

---

## 📁 Project Structure

backend-school-chatbot-local-llm/
│
├── main.py  
├── config.py  
├── models.py  
├── routes/  
│   ├── api_routes.py  
│   └── file_routes.py  
├── services/  
│   ├── llm_service.py  
│   ├── pdf_rag_service.py  
│   └── query_executor.py  
├── requirements.txt  
└── README.md  

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/EugheneH04/school_chatbot_with_llm.git
cd school_chatbot_with_llm
2. Create Virtual Environment
Using venv:

python -m venv venv
venv\Scripts\activate
Using conda:

conda create -n school-chatbot python=3.11
conda activate school-chatbot
3. Install Dependencies
pip install -r requirements.txt
▶️ Run the Application
uvicorn main:app --reload
Application runs at:

http://127.0.0.1:8000

Swagger Docs:

http://127.0.0.1:8000/docs

🤖 LLM Setup (Ollama)
Make sure Ollama is installed and running.

Pull model:

ollama pull llama3.1:8b
or

ollama pull qwen2.5:7b
📌 API Endpoints
Upload PDF
POST /api/v1/files/upload

Ask Question
POST /api/v1/ask

🔒 Environment Variables
Create a .env file:

MODEL_NAME=llama3.1:8b

📈 Future Enhancements
Authentication & Role Management

Database Integration

Cloud Deployment

UI Dashboard

CI/CD Pipeline

