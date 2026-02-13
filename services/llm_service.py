"""
LLM service for making API calls to Ollama.
Handles all interactions with the language model.
"""
import httpx
import json
import re
from typing import Dict, Any

from config import settings
from prompts import QUERY_PLANNER_PROMPT, RESPONSE_GENERATOR_PROMPT

class LLMService:
    """Service for interacting with the LLM"""
    
    def __init__(self):
        self.url = settings.OLLAMA_URL
        self.model = settings.OLLAMA_MODEL
        self.timeout = httpx.Timeout(settings.OLLAMA_TIMEOUT)
    
    async def get_structured_query(self, question: str) -> Dict[str, Any]:
        """
        Convert natural language question to structured query.
        
        Args:
            question: User's natural language question
            
        Returns:
            Structured query as dictionary
            
        Raises:
            Exception: If LLM response is invalid
        """
        prompt = QUERY_PLANNER_PROMPT + "\nUser Question:\n" + question
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                self.url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json"  # Force JSON output
                },
            )
            data = response.json()
            
            if "response" not in data:
                raise Exception("Invalid Ollama response: " + str(data))
            
            raw_output = data["response"].strip()
            
            if not raw_output:
                raise Exception("Model returned empty response")
            
            # Try direct JSON parse
            try:
                return json.loads(raw_output)
            except json.JSONDecodeError:
                # Extract JSON with regex as fallback
                match = re.search(r"\{.*\}", raw_output, re.DOTALL)
                if match:
                    return json.loads(match.group())
                raise Exception("No valid JSON found in model output:\n" + raw_output)
    
    async def generate_natural_response(self, question: str, result: Any) -> str:
        """
        Convert query result to natural language response.
        
        Args:
            question: Original user question
            result: Query result (can be number, dict, list, or None)
            
        Returns:
            Natural language response string
        """
        # Format result for LLM
        if result is None:
            formatted_result = "No data found"
        elif isinstance(result, dict) and "error" in result:
            formatted_result = f"Error - {result['error']}"
        elif isinstance(result, list):
            formatted_result = json.dumps(result, indent=2)
        elif isinstance(result, float):
            formatted_result = str(round(result, 2))
        else:
            formatted_result = str(result)
        
        # Create prompt
        prompt = RESPONSE_GENERATOR_PROMPT.format(
            question=question,
            result=formatted_result
        )
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                self.url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
            )
            data = response.json()
            
            if "response" not in data:
                return f"The result is: {result}"
            
            # Clean up response
            response_text = data["response"].strip()
            
            # Remove common prefixes
            prefixes_to_remove = [
                "Response:",
                "Here's a response:",
                "Here's a friendly response:",
                "The user asked",
                "It looks like"
            ]
            
            for prefix in prefixes_to_remove:
                if response_text.startswith(prefix):
                    response_text = response_text[len(prefix):].strip()
            
            # Remove quotes if entire response is quoted
            if response_text.startswith('"') and response_text.endswith('"'):
                response_text = response_text[1:-1]
            
            return response_text

# Create singleton instance
llm_service = LLMService()