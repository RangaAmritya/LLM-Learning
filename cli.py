import sys
import logging
import argparse
from chat_bot import ChatBot
from models import ChatBotError, Provider
from config import DEFAULT_PROVIDER, DEFAULT_MODEL

logger = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser(description="Chat with different LLM models")
    parser.add_argument(
        "--provider",
        choices=[p.value for p in Provider],
        default=DEFAULT_PROVIDER,
        help="LLM provider to use"
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help="Model name to use"
    )
    return parser.parse_args()

def start_cli_chat() -> None:
    """Start interactive chat session"""
    try:
        args = parse_args()
        chat_bot = ChatBot(model_name=args.model, provider=args.provider)
        
        print(f"Chat initialized with {args.provider} provider and {args.model} model")
        print("Type 'quit' to exit")
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
                response = chat_bot.generate_response(user_input)
                print("\nAssistant:", response)
                print("-" * 50)
            except ChatBotError as e:
                print(f"\nError: {str(e)}")
                print("-" * 50)
                
    except KeyboardInterrupt:
        logger.info("Chat session terminated by keyboard interrupt")
        print("\nGoodbye!")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        print(f"\nAn unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    start_cli_chat() 