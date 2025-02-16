import streamlit as st
from chat_bot import ChatBot
from models import Provider
from config import DEFAULT_MODEL, DEFAULT_PROVIDER
import time

def initialize_session_state():
    """Initialize the session state variables"""
    if "chat_bot" not in st.session_state:
        st.session_state.chat_bot = ChatBot(
            model_name=st.session_state.get("model_name", DEFAULT_MODEL),
            provider=st.session_state.get("provider", DEFAULT_PROVIDER)
        )
    if "messages" not in st.session_state:
        st.session_state.messages = []

def main():
    st.set_page_config(page_title="LLM Chat Bot", page_icon="🤖")
    
    st.title("🤖 Local LLM Chat Bot")
    
    # Sidebar for model selection
    with st.sidebar:
        st.title("Settings")
        
        # Provider selection
        provider = st.selectbox(
            "Choose your provider",
            [p.value for p in Provider],
            key="provider"
        )
        
        # Model selection based on provider
        if provider == Provider.OPENAI.value:
            model_options = ["gpt-3.5-turbo", "gpt-4"]
        else:
            model_options = ["llama3.2", "deepseek-r1:1.5b"]
            
        model_name = st.selectbox(
            "Choose your model",
            model_options,
            key="model_name"
        )
        
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.session_state.chat_bot = ChatBot(
                model_name=model_name,
                provider=provider
            )
    
    # Initialize session state
    initialize_session_state()
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.chat_bot.generate_response(prompt)
                    st.write(response)
                    
                    # Add assistant response to history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 