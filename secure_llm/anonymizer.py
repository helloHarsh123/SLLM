from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from typing import Dict, Tuple

class PromptAnonymizer:
    def __init__(self):
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()
        self._mapping = {}
        self._reverse_mapping = {}
        
    def anonymize(self, text: str) -> Tuple[str, Dict]:
        # Analyze text with presidio
        analyzer_results = self.analyzer.analyze(
            text=text,
            language='en',
            entities=["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER", 
                     "CREDIT_CARD", "LOCATION", "DATE_TIME"]
        )
        
        # Anonymize the identified entities
        anonymized_text = self.anonymizer.anonymize(
            text=text,
            analyzer_results=analyzer_results
        ).text
        
        # Store mapping for later de-anonymization
        for result in analyzer_results:
            original = text[result.start:result.end]
            anonymized = f"<{result.entity_type}_{len(self._mapping)}>"
            self._mapping[anonymized] = original
            self._reverse_mapping[original] = anonymized
            
        return anonymized_text, self._mapping
    
    def deanonymize(self, text: str) -> str:
        deanonymized = text
        for anon, original in self._mapping.items():
            deanonymized = deanonymized.replace(anon, original)
        return deanonymized