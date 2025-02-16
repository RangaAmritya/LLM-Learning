from dataclasses import dataclass
from typing import List, Literal
from enum import Enum

ProviderType = Literal["ollama", "openai"]

class Provider(Enum):
    OLLAMA = "ollama"
    OPENAI = "openai"

@dataclass
class Message:
    user: str
    assistant: str

class ChatBotError(Exception):
    """Custom exception for ChatBot related errors"""
    pass 