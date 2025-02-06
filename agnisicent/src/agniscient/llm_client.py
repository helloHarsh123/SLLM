import openai
from typing import Optional
from .config import Config
from .anonymizer import PromptAnonymizer
from .database import Database
import base64

class SecureLLMClient:
    def __init__(self, config: Config):
        # Generate encryption key from our_key
        encryption_key = base64.urlsafe_b64encode(config.our_key.encode()[:32].ljust(32, b'0'))
        
        self.openai_client = openai.OpenAI(api_key=config.openai_key)
        self.anonymizer = PromptAnonymizer()
        self.db = Database(config.db_connection_string, encryption_key.decode())
        
    def generate_response(self, 
                         prompt: str, 
                         model: str = "gpt-4o-mini",
                         max_tokens: Optional[int] = None) -> str:
        # Anonymize the prompt
        anonymized_prompt, mapping = self.anonymizer.anonymize(prompt)
        
        # Make the API call
        response = self.openai_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": anonymized_prompt}],
            max_tokens=max_tokens
        )
        
        # Get the response text
        response_text = response.choices[0].message.content
        
        # De-anonymize the response
        deanonymized_response = self.anonymizer.deanonymize(response_text)
        
        # Store the call in the database
        self.db.store_call(
            original_prompt=prompt,
            anonymized_prompt=anonymized_prompt,
            response=deanonymized_response,
            mapping=mapping
        )
        
        return deanonymized_response
    
    def get_history(self):
        return self.db.get_call_history()