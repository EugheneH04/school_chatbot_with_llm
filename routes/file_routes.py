"""
File upload routes.
Handles PDF and Excel uploads and connects them to RAG service.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from models import QuestionRequest, QuestionResponse
from pypdf import PdfReader
import pandas as pd
import io

from services.pdf_rag_service import (
    create_vectorstore_from_text,
    create_pdf_conversation_chain
)
from config import settings

router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload PDF or Excel file and initialize RAG pipeline.
    """

    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    filename = file.filename.lower()

    try:
        # -------------------------
        # 📄 Handle PDF
        # -------------------------
        if filename.endswith(".pdf"):

            pdf_reader = PdfReader(file.file)
            text = ""

            for page in pdf_reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted

            if not text.strip():
                raise HTTPException(status_code=400, detail="PDF contains no readable text")

            # Create RAG pipeline
            vectorstore = create_vectorstore_from_text(text)
            conversation_chain = create_pdf_conversation_chain(vectorstore)

            # Store chain in memory
            settings.set_pdf_chain(conversation_chain)

            return {
                "status": "success",
                "message": "PDF uploaded and RAG initialized successfully."
            }

        # -------------------------
        # 📊 Handle Excel
        # -------------------------
        elif filename.endswith(".xlsx") or filename.endswith(".xls"):

            contents = await file.read()
            excel_file = pd.read_excel(io.BytesIO(contents))

            if excel_file.empty:
                raise HTTPException(status_code=400, detail="Excel file is empty")

            # Convert dataframe to text
            text = excel_file.to_string(index=False)

            vectorstore = create_vectorstore_from_text(text)
            chain = create_pdf_conversation_chain(vectorstore)

            settings.set_pdf_chain(chain)

            return {
                "status": "success",
                "message": "Excel uploaded and RAG initialized successfully."
            }

        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Upload PDF or Excel.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from models import QuestionRequest, QuestionResponse


@router.post("/ask", response_model=QuestionResponse)
async def ask_pdf_question(request: QuestionRequest):

    print("📌 PDF Question:", request.question)  # ✅ ADD HERE

    conversation_chain = settings.get_pdf_chain()

    if conversation_chain is None:
        print("❌ No PDF chain found")  # ✅ ADD HERE
        raise HTTPException(status_code=400, detail="No PDF uploaded yet.")

    print("🔁 Using existing PDF chain")  # ✅ ADD HERE

    response = conversation_chain.invoke(
        {"question": request.question, "chat_history": []}
    )

    print("🧠 Raw RAG Response:", response)  # ✅ ADD HERE

    return QuestionResponse(
        response=response["answer"],
        structured_query=None,
        raw_result=None
    )
