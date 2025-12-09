import ollama
from typing import List, Dict

class LLMHandler:
    def __init__(self, model_name: str = "llama3.2:3b"):
        self.model_name = model_name
    
    def set_model(self, model_name: str):
        self.model_name = model_name
    
    def generate_response(self, prompt: str, context: List[str]) -> str:
        context_text = "\n\n".join([f"[Source {i+1}]: {ctx}" for i, ctx in enumerate(context)])
        
        full_prompt = f"""You are a helpful AI assistant that answers questions based on the provided context.

Context:
{context_text}

Question: {prompt}

Instructions:
- Answer the question using ONLY the information from the context above
- If the answer is not in the context, say "I cannot find this information in the provided documents"
- Cite the source numbers [Source 1], [Source 2], etc. when referencing information
- Be concise and accurate

Answer:"""
        
        response = ollama.generate(
            model=self.model_name,
            prompt=full_prompt
        )
        
        return response['response']
    
    def summarize_document(self, text: str) -> str:
        prompt = f"""Summarize the following document in a concise manner. Focus on the key points and main ideas.

Document:
{text[:4000]}

Summary:"""
        
        response = ollama.generate(
            model=self.model_name,
            prompt=prompt
        )
        
        return response['response']
    
    def check_model_availability(self) -> bool:
        try:
            ollama.list()
            return True
        except:
            return False
