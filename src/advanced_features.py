from typing import List, Dict, Tuple
import time

class DocumentComparison:
    def __init__(self, llm_handler):
        self.llm = llm_handler
    
    def compare_documents(self, doc1_chunks: List[str], doc2_chunks: List[str], 
                         doc1_name: str, doc2_name: str, aspect: str) -> str:
        
        doc1_sample = " ".join(doc1_chunks[:3])[:2000]
        doc2_sample = " ".join(doc2_chunks[:3])[:2000]
        
        prompt = f"""Compare the following two documents on the aspect: {aspect}

Document 1 ({doc1_name}):
{doc1_sample}

Document 2 ({doc2_name}):
{doc2_sample}

Provide a detailed comparison highlighting:
1. Similarities
2. Differences
3. Key insights

Comparison:"""
        
        import ollama
        response = ollama.generate(
            model=self.llm.model_name,
            prompt=prompt
        )
        
        return response['response']
    
    def find_contradictions(self, chunks: List[str], metadatas: List[Dict]) -> List[Dict]:
        contradictions = []
        
        return contradictions
    
    def extract_key_differences(self, doc1_text: str, doc2_text: str) -> Dict:
        return {
            "length_diff": abs(len(doc1_text) - len(doc2_text)),
            "word_count_diff": abs(len(doc1_text.split()) - len(doc2_text.split()))
        }

class ConfidenceScorer:
    def __init__(self):
        self.threshold_high = 0.8
        self.threshold_medium = 0.5
    
    def calculate_confidence(self, sources: List[Dict], answer: str) -> Dict:
        if not sources:
            return {"score": 0.0, "level": "low", "reason": "No sources found"}
        
        num_sources = len(sources)
        
        answer_length = len(answer.split())
        
        if "cannot find" in answer.lower() or "not in the" in answer.lower():
            confidence = 0.3
            level = "low"
            reason = "AI indicated information not found"
        elif num_sources >= 3 and answer_length > 20:
            confidence = 0.9
            level = "high"
            reason = f"Multiple sources ({num_sources}) with detailed answer"
        elif num_sources >= 2:
            confidence = 0.7
            level = "medium"
            reason = f"Moderate sources ({num_sources})"
        else:
            confidence = 0.5
            level = "medium"
            reason = "Single source"
        
        return {
            "score": confidence,
            "level": level,
            "reason": reason,
            "num_sources": num_sources
        }
