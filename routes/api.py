"""
API routes for the application.
Defines all HTTP endpoints.
"""
from fastapi import APIRouter
import json

from models import QuestionRequest, QuestionResponse
from services import llm_service, query_executor

router = APIRouter()

@router.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """
    Answer a natural language question about the student data.
    
    Process:
    1. Convert question to structured query using LLM
    2. Execute query on DataFrame safely
    3. Convert result to natural language using LLM
    
    Args:
        request: QuestionRequest containing the user's question
        
    Returns:
        QuestionResponse with natural language answer and debug info
    """
    print(f"Question: {request.question}")
    
    # Step 1: Get structured query from LLM
    structured_query = await llm_service.get_structured_query(request.question)
    print(f"Structured Query: {json.dumps(structured_query, indent=2)}")
    
    # Step 2: Execute query on DataFrame
    result = query_executor.execute(structured_query)
    print(f"Result: {result}")
    
    # Step 3: Generate natural language response
    natural_response = await llm_service.generate_natural_response(
        request.question, 
        result
    )
    print(f"Natural Response: {natural_response}")
    
    return QuestionResponse(
        response=natural_response,
        structured_query=structured_query,
        raw_result=result
    )

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}