from langchain_experimental.data_anonymizer import PresidioReversibleAnonymizer
class PromptAnonymizer:
    def __init__(self):
        self.anonymizer = PresidioReversibleAnonymizer(
            analyzed_fields=["PERSON", "PHONE_NUMBER", "EMAIL_ADDRESS", "CREDIT_CARD"],
            faker_seed=42,
        )
        
    def anonymize(self, text: str) -> str:
        return self.anonymizer.anonymize(text)
    
    def deanonymize(self, text: str) -> str:
        return self.anonymizer.deanonymize(text)