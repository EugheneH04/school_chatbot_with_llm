# 📚 School Chatbot with Local LLM

An AI-powered school management chatbot built using **FastAPI**, **Local LLM (Ollama)**, and intelligent query processing.

This chatbot can:

* Answer student-related queries
* Process uploaded PDF documents (RAG)
* Execute structured data queries
* Switch between different LLM models
* Handle real-time conversational queries

---

## 🚀 Features

* 🔹 FastAPI backend
* 🔹 Local LLM integration (Ollama)
* 🔹 Multi-model support
* 🔹 PDF Question Answering (RAG)
* 🔹 Structured query execution
* 🔹 Modular architecture
* 🔹 REST API endpoints

---

## 🏗️ Project Structure

```
backend-school-chatbot-local-llm/
│
├── main.py
├── config.py
├── models.py
├── routes/
│   ├── file_routes.py
│   └── api_routes.py
├── services/
│   ├── llm_service.py
│   ├── pdf_rag_service.py
│   └── query_executor.py
├── requirements.txt
└── README.md
```

---

## 🧠 How It Works

1. User sends a question via API
2. System classifies the query
3. Based on query type:

   * Structured query → executed via query executor
   * Document query → processed using RAG
   * General query → sent to LLM
4. LLM generates contextual response

---

## ⚙️ Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/EugheneH04/school_chatbot_with_llm.git
cd school_chatbot_with_llm
```

---

### 2️⃣ Create Virtual Environment

Using venv:

```bash
python -m venv venv
venv\Scripts\activate
```

Or using conda:

```bash
conda create -n school-chatbot python=3.11
conda activate school-chatbot
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Start FastAPI Server

```bash
uvicorn main:app --reload
```

Server will run at:

```
http://127.0.0.1:8000
```

---

## 🤖 LLM Setup (Ollama)

Make sure Ollama is installed and running.

Pull required model:

```bash
ollama pull llama3.1:8b
```

or

```bash
ollama pull qwen2.5:7b
```

---

## 📂 API Endpoints

### Upload File

```
POST /api/v1/files/upload
```

### Ask Question

```
POST /api/v1/ask
```

---

## 🔒 Environment Variables

Create `.env` file:

```
MODEL_NAME=llama3.1:8b
```

---

## 🧪 Future Improvements

* Authentication system
* Role-based access
* Database integration
* Cloud deployment
* CI/CD pipeline
* UI Dashboard

---

## 👨‍💻 Author

**Midhun Suresh**
Aspiring Data Analyst & AI Developer

---

## 📜 License

This project is for educational and research purposes.

---

# 🔥 Optional (Better Version)

If you want, I can also:

* Make it more professional for recruiters
* Add architecture diagram
* Add API request/response examples
* Add deployment instructions (Render / AWS / GCP)
* Make it enterprise-level documentation

Tell me where you're planning to showcase this (GitHub portfolio / resume / client demo) 🚀


