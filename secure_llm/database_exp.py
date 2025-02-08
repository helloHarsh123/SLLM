from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from cryptography.fernet import Fernet
import json

Base = declarative_base()

class LLMCall(Base):
    __tablename__ = 'llm_calls'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    original_prompt = Column(String)
    anonymized_prompt = Column(String)
    anonymized_response = Column(String)
    response = Column(String)
    
class Database:
    def __init__(self, connection_string: str, encryption_key: str):
        self.engine = create_engine(connection_string)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.fernet = Fernet(encryption_key.encode())
        
    def store_call(self, original_prompt: str, anonymized_prompt: str, anonymized_response: str,
                   response: str):
        session = self.Session()
        
        # Encrypt sensitive data
        encrypted_prompt = self.fernet.encrypt(original_prompt.encode()).decode()
        encrypted_response = self.fernet.encrypt(response.encode()).decode()
        
        call = LLMCall(
            original_prompt=encrypted_prompt,
            anonymized_prompt=anonymized_prompt,
            anonymized_response=anonymized_response,
            response=encrypted_response,
        )
        
        session.add(call)
        session.commit()
        session.close()
    
    def get_call_history(self):
        session = self.Session()
        calls = session.query(LLMCall).all()
        
        decrypted_calls = []
        for call in calls:
            decrypted_calls.append({
                'timestamp': call.timestamp,
                'original_prompt': self.fernet.decrypt(call.original_prompt.encode()).decode(),
                'anonymized_prompt': call.anonymized_prompt,
                'anonymized_response': call.anonymized_response,
                'response': self.fernet.decrypt(call.response.encode()).decode()
            })
            
        session.close()
        return decrypted_calls