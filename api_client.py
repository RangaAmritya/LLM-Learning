import requests
from openai import OpenAI
from typing import Dict
import logging
from config import (
    OLLAMA_API_URL, 
    OLLAMA_TIMEOUT, 
    OPENAI_API_KEY, 
    OPENAI_TIMEOUT,
    OPENAI_DEFAULT_MODEL,
    OPENAI_SYSTEM_PROMPT
)
from models import ChatBotError
from llm_providers import LLMProvider

logger = logging.getLogger(__name__)

class OllamaClient(LLMProvider):
    def generate_response(self, model_name: str, prompt: str) -> Dict:
        """
        Make API request to Ollama
        
        Args:
            model_name: Name of the model to use
            prompt: The complete prompt to send
            
        Returns:
            API response as dictionary
        """
        try:
            response = requests.post(
                f"{OLLAMA_API_URL}/generate",
                json={
                    "model": model_name,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=OLLAMA_TIMEOUT
            )
            response.raise_for_status()
            return {"response": response.json()["response"]}
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama API request failed: {str(e)}")
            raise ChatBotError(f"Failed to generate response: {str(e)}")

class OpenAIClient(LLMProvider):
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ChatBotError("OpenAI API key not found in environment variables")
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def generate_response(self, model_name: str, prompt: str) -> Dict:
        """
        Make API request to OpenAI
        
        Args:
            model_name: Name of the model to use
            prompt: The complete prompt to send
            
        Returns:
            API response as dictionary
        """
        try:
            response = self.client.chat.completions.create(
                model=model_name or OPENAI_DEFAULT_MODEL,
                messages=[
                    {"role": "system", "content": OPENAI_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                timeout=OPENAI_TIMEOUT
            )
            return {"response": response.choices[0].message.content}
            
        except Exception as e:
            logger.error(f"OpenAI API request failed: {str(e)}")
            raise ChatBotError(f"Failed to generate response: {str(e)}")

def get_llm_provider(provider: str) -> LLMProvider:
    """Factory function to get the appropriate LLM provider"""
    providers = {
        "ollama": OllamaClient,
        "openai": OpenAIClient
    }
    
    if provider not in providers:
        raise ChatBotError(f"Unknown provider: {provider}")
        
    return providers[provider]() 