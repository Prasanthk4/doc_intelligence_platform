import chromadb
from chromadb.config import Settings
from typing import List, Dict
from config.config import CHROMA_DIR, RETRIEVAL_TOP_K

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=CHROMA_DIR,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = None
    
    def create_collection(self, collection_name: str = "documents"):
        try:
            self.client.delete_collection(name=collection_name)
        except:
            pass
        
        self.collection = self.client.create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        return self.collection
    
    def get_or_create_collection(self, collection_name: str = "documents"):
        try:
            self.collection = self.client.get_collection(name=collection_name)
        except:
            self.collection = self.create_collection(collection_name)
        return self.collection
    
    def add_documents(self, chunks: List[str], metadatas: List[Dict], embeddings: List):
        ids = [f"doc_{i}" for i in range(len(chunks))]
        
        self.collection.add(
            documents=chunks,
            metadatas=metadatas,
            embeddings=embeddings,
            ids=ids
        )
    
    def search(self, query_embedding: List[float], top_k: int = RETRIEVAL_TOP_K) -> Dict:
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        return results
    
    def get_collection_count(self) -> int:
        if self.collection:
            return self.collection.count()
        return 0
    
    def clear_collection(self):
        if self.collection:
            collection_name = self.collection.name
            self.client.delete_collection(name=collection_name)
            self.collection = self.create_collection(collection_name)
