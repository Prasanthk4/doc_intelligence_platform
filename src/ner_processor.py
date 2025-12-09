import spacy
from typing import List, Dict
from collections import Counter

class NERProcessor:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            import os
            os.system("python -m spacy download en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        doc = self.nlp(text)
        
        entities = {
            "PERSON": [],
            "ORG": [],
            "DATE": [],
            "MONEY": [],
            "GPE": [],
            "PRODUCT": []
        }
        
        for ent in doc.ents:
            if ent.label_ in entities:
                entities[ent.label_].append(ent.text)
        
        return entities
    
    def get_entity_summary(self, text: str) -> Dict:
        entities = self.extract_entities(text)
        
        summary = {}
        for entity_type, values in entities.items():
            if values:
                counter = Counter(values)
                summary[entity_type] = {
                    "count": len(values),
                    "unique": len(counter),
                    "most_common": counter.most_common(5)
                }
        
        return summary
    
    def extract_from_multiple_docs(self, documents: List[str]) -> Dict:
        all_entities = {
            "PERSON": [],
            "ORG": [],
            "DATE": [],
            "MONEY": [],
            "GPE": [],
            "PRODUCT": []
        }
        
        for doc_text in documents:
            entities = self.extract_entities(doc_text)
            for entity_type, values in entities.items():
                all_entities[entity_type].extend(values)
        
        summary = {}
        for entity_type, values in all_entities.items():
            if values:
                counter = Counter(values)
                summary[entity_type] = counter.most_common(10)
        
        return summary
