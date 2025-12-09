from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np
from config.config import EMBEDDING_MODEL

class EmbeddingGenerator:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        self.dimension = self.model.get_sentence_embedding_dimension()
    
    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        embeddings = self.model.encode(texts, show_progress_bar=True)
        return embeddings
    
    def generate_single_embedding(self, text: str) -> np.ndarray:
        embedding = self.model.encode([text])[0]
        return embedding
    
    def get_embedding_dimension(self) -> int:
        return self.dimension
