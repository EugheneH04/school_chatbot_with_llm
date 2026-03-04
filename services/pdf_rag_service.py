"""
PDF RAG Service
Handles chunking and answering questions from PDF text.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_classic.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain_core.prompts import PromptTemplate

# ------------------ PROMPT ------------------

template = """
You are a helpful assistant.
Answer ONLY using the provided context.
If the answer is not in the context, say "Answer not found in document."

Context:
{context}

Question:
{question}
"""

QA_PROMPT = PromptTemplate(
    template=template,
    input_variables=["context", "question"]
)

# ------------------ VECTOR STORE ------------------

def create_vectorstore_from_text(text: str):

    print("TEXT LENGTH:", len(text))

    if not text.strip():
        raise ValueError("PDF text is empty")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    chunks = text_splitter.split_text(text)

    print("CHUNKS CREATED:", len(chunks))

    if not chunks:
        raise ValueError("No chunks created from PDF")

    embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")

    print("Creating FAISS...")
    vectorstore = FAISS.from_texts(chunks, embedding=embeddings)
    print("FAISS created successfully")

    return vectorstore

# ------------------ CONVERSATION CHAIN ------------------

def create_pdf_conversation_chain(vectorstore):

    llm = ChatOllama(model="qwen2.5:7b")

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 6, "fetch_k": 12}
    )

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        combine_docs_chain_kwargs={"prompt": QA_PROMPT},
        return_source_documents=True
    )

    return conversation_chain

# ------------------ ASK QUESTION ------------------

def ask_pdf_question(conversation_chain, question: str, chat_history):

    response = conversation_chain(
        {"question": question, "chat_history": chat_history}
    )

    print("Sources Used:")
    for doc in response["source_documents"]:
        print(doc.page_content[:300])

    return response["answer"]
