from abc import ABC, abstractmethod
from typing import Dict
import logging
from models import ChatBotError

logger = logging.getLogger(__name__)

class LLMProvider(ABC):
    @abstractmethod
    def generate_response(self, model_name: str, prompt: str) -> Dict:
        """Generate response from the LLM model"""
        pass 