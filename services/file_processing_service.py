"""
File Processing Service
Handles PDF, Excel, and CSV uploads.
Refactored from GitHub repo processing_file.py
"""

import pandas as pd
from pypdf import PdfReader
from fastapi import UploadFile
from typing import Union
from io import BytesIO


async def process_uploaded_file(file: UploadFile) -> Union[str, pd.DataFrame]:
    """
    Detect file type and process accordingly.
    """

    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        return await process_pdf(file)

    elif filename.endswith(".xlsx") or filename.endswith(".xls"):
        return await process_excel(file)

    elif filename.endswith(".csv"):
        return await process_csv(file)

    else:
        raise ValueError("Unsupported file type")


# ---------------- PDF ---------------- #

async def process_pdf(file: UploadFile) -> str:
    """
    Extract text from uploaded PDF.
    """
    pdf_bytes = await file.read()
    reader = PdfReader(BytesIO(pdf_bytes))

    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted

    return text


# ---------------- Excel ---------------- #

async def process_excel(file: UploadFile) -> pd.DataFrame:
    """
    Load Excel file into DataFrame.
    """
    excel_bytes = await file.read()
    df = pd.read_excel(BytesIO(excel_bytes))
    return df


# ---------------- CSV ---------------- #

async def process_csv(file: UploadFile) -> pd.DataFrame:
    """
    Load CSV file into DataFrame.
    """
    csv_bytes = await file.read()
    df = pd.read_csv(BytesIO(csv_bytes))
    return df
