import logging
from typing import List, Dict
import sys
from models import Message, ChatBotError, Provider
from api_client import get_llm_provider
from config import DEFAULT_PROVIDER, DEFAULT_MODEL, OPENAI_SYSTEM_PROMPT

logger = logging.getLogger(__name__)

class ChatBot:
    def __init__(self, model_name: str = DEFAULT_MODEL, provider: str = DEFAULT_PROVIDER):
        """
        Initialize ChatBot with specified model and provider
        
        Args:
            model_name: Name of the LLM model to use
            provider: Name of the LLM provider (ollama or openai)
        """
        self.model_name = model_name
        self.provider = provider
        self.history: List[Message] = []
        self.llm_provider = get_llm_provider(provider)
        logger.info(f"ChatBot initialized with {provider} provider and {model_name} model")
        
    def _build_prompt(self, user_input: str) -> str | List[Dict]:
        """
        Build the complete prompt including conversation history
        
        Args:
            user_input: Current user input
            
        Returns:
            Complete prompt string or message list for OpenAI
        """
        if self.provider == Provider.OPENAI.value:
            messages = [{"role": "system", "content": OPENAI_SYSTEM_PROMPT}]
            for msg in self.history:
                messages.extend([
                    {"role": "user", "content": msg.user},
                    {"role": "assistant", "content": msg.assistant}
                ])
            messages.append({"role": "user", "content": user_input})
            return messages
        else:
            conversation = "\n".join([
                f"User: {msg.user}\nAssistant: {msg.assistant}"
                for msg in self.history
            ])
            return f"{conversation}\nUser: {user_input}\nAssistant:" if conversation else f"User: {user_input}\nAssistant:"

    def generate_response(self, prompt: str) -> str:
        """
        Generate response for user input
        
        Args:
            prompt: User input text
            
        Returns:
            Generated response text
        """
        try:
            full_prompt = self._build_prompt(prompt)
            result = self.llm_provider.generate_response(self.model_name, full_prompt)
            
            # Store the conversation
            self.history.append(Message(
                user=prompt,
                assistant=result["response"]
            ))
            
            logger.debug(f"Generated response for prompt: {prompt[:50]}...")
            return result["response"]
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return f"I apologize, but I encountered an error: {str(e)}"

    def clear_history(self) -> None:
        """Clear conversation history"""
        self.history = []
        logger.info("Conversation history cleared")

    def chat(self) -> None:
        """Start interactive chat session"""
        logger.info(f"Starting chat session with {self.model_name} model")
        print(f"Chat initialized with {self.model_name} model. Type 'quit' to exit.")
        print("-" * 50)
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit']:
                logger.info("Chat session ended by user")
                print("Goodbye!")
                break
                
            if not user_input:
                continue
                
            try:
                response = self.generate_response(user_input)
                print("\nAssistant:", response)
                print("-" * 50)
            except ChatBotError as e:
                print(f"\nError: {str(e)}")
                print("-" * 50)

def main() -> None:
    try:
        model_name = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MODEL
        provider = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_PROVIDER
        chat_bot = ChatBot(model_name, provider)
        chat_bot.chat()
    except KeyboardInterrupt:
        logger.info("Chat session terminated by keyboard interrupt")
        print("\nGoodbye!")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        print(f"\nAn unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main() 