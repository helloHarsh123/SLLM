from secure_llm.config import Config
from secure_llm.llm_client import SecureLLMClient
import os
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    open_ai_key = os.getenv('OPEN_AI_KEY')
    config = Config(
        openai_key=open_ai_key,
        our_key="hg12345"
    )
    
    client = SecureLLMClient(config)
    
    # Example prompt with sensitive information
    response = client.generate_response(
        "My name is John Doe and my email is john@example.com. "
        "Can you help me write a professional bio?"
    )
    
    print("Response:", response)
    
    # Get history of all calls
    history = client.get_history()
    print("\nHistory:", history)