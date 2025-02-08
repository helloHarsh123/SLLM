from secure_llm.config import Config
from secure_llm.llm_client_exp import SecureLLMClient
import os
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    open_ai_key = os.getenv('OPEN_AI_KEY')
    config = Config(
        openai_key=open_ai_key,
        our_key="hg123456"
    )
    
    client = SecureLLMClient(config)
    
    # Example prompt with sensitive information
    response = client.generate_response(
        "Hey I am Harsh Gupta. I recently had a patient Rishabh Oberoi(Phone: 9871671891), 23 years old, but had serious joint pains"
        ", what could be the issue here?"
        "Rewrite this text into an official, short email:"
    )
    
    print("Response:", response)
    
    # Get history of all calls
    history = client.get_history()
    for(item) in history:
        print(item)
    #print("\nHistory:", history)