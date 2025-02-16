import os
from dotenv import load_dotenv
import logging

# Configure logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(override=True)

# Provider Configuration
DEFAULT_PROVIDER = os.getenv("DEFAULT_PROVIDER", "ollama")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "llama3.2")

# Ollama Configuration
OLLAMA_API_URL = "http://localhost:11434/api"
OLLAMA_TIMEOUT = 30

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_TIMEOUT = 30
OPENAI_DEFAULT_MODEL = "gpt-3.5-turbo"
OPENAI_SYSTEM_PROMPT = "You are a helpful AI assistant."

# Validate OpenAI API Key
if OPENAI_API_KEY and OPENAI_API_KEY.startswith('sk-') and len(OPENAI_API_KEY) > 20:
    logger.info("OpenAI API key looks valid")
else:
    logger.warning("OpenAI API key might be invalid or missing") 