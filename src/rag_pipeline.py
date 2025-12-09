from typing import List, Dict, Tuple
import time
from src.document_processor import DocumentProcessor
from src.embeddings import EmbeddingGenerator
from src.vector_store import VectorStore
from src.llm_handler import LLMHandler
from src.performance import QueryCache, PerformanceTracker
from src.advanced_features import ConfidenceScorer, DocumentComparison

class RAGPipeline:
    def __init__(self, model_name: str = "llama3.2:3b"):
        self.doc_processor = DocumentProcessor()
        self.embedding_gen = EmbeddingGenerator()
        self.vector_store = VectorStore()
        self.llm = LLMHandler(model_name)
        self.vector_store.get_or_create_collection()
        self.cache = QueryCache(max_size=100)
        self.perf_tracker = PerformanceTracker()
        self.confidence_scorer = ConfidenceScorer()
        self.doc_comparison = DocumentComparison(self.llm)
    
    def set_model(self, model_name: str):
        self.llm.set_model(model_name)
    
    def ingest_documents(self, file_paths: List[str]) -> Dict:
        processed_docs = self.doc_processor.process_multiple_documents(file_paths)
        
        all_chunks = []
        all_metadatas = []
        
        for doc in processed_docs:
            for i, chunk in enumerate(doc['chunks']):
                all_chunks.append(chunk)
                all_metadatas.append({
                    "filename": doc['filename'],
                    "chunk_id": i,
                    "total_chunks": doc['num_chunks']
                })
        
        embeddings = self.embedding_gen.generate_embeddings(all_chunks)
        
        self.vector_store.add_documents(all_chunks, all_metadatas, embeddings.tolist())
        
        return {
            "num_documents": len(processed_docs),
            "num_chunks": len(all_chunks),
            "documents": [doc['filename'] for doc in processed_docs],
            "processed_docs": processed_docs
        }
    
    def query(self, question: str, use_cache: bool = True) -> Tuple[str, List[Dict], Dict]:
        start_time = time.time()
        
        if use_cache:
            cached_result = self.cache.get(question)
            if cached_result:
                answer, sources = cached_result
                confidence = self.confidence_scorer.calculate_confidence(sources, answer)
                return answer, sources, confidence
        
        query_embedding = self.embedding_gen.generate_single_embedding(question)
        
        search_results = self.vector_store.search(query_embedding.tolist())
        
        contexts = search_results['documents'][0]
        metadatas = search_results['metadatas'][0]
        
        answer = self.llm.generate_response(question, contexts)
        
        sources = []
        for i, (ctx, meta) in enumerate(zip(contexts, metadatas)):
            sources.append({
                "source_number": i + 1,
                "filename": meta['filename'],
                "chunk_id": meta['chunk_id'],
                "text": ctx[:200] + "..." if len(ctx) > 200 else ctx
            })
        
        if use_cache:
            self.cache.set(question, (answer, sources))
        
        query_time = time.time() - start_time
        self.perf_tracker.track_query_time(query_time)
        
        confidence = self.confidence_scorer.calculate_confidence(sources, answer)
        
        return answer, sources, confidence
    
    def summarize_document(self, filename: str) -> str:
        results = self.vector_store.collection.get(
            where={"filename": filename}
        )
        
        if not results['documents']:
            return "Document not found"
        
        full_text = " ".join(results['documents'][:5])
        summary = self.llm.summarize_document(full_text)
        
        return summary
    
    def compare_documents(self, doc1_name: str, doc2_name: str, aspect: str) -> str:
        doc1_results = self.vector_store.collection.get(where={"filename": doc1_name})
        doc2_results = self.vector_store.collection.get(where={"filename": doc2_name})
        
        if not doc1_results['documents'] or not doc2_results['documents']:
            return "One or both documents not found"
        
        comparison = self.doc_comparison.compare_documents(
            doc1_results['documents'],
            doc2_results['documents'],
            doc1_name,
            doc2_name,
            aspect
        )
        
        return comparison
    
    def get_stats(self) -> Dict:
        count = self.vector_store.get_collection_count()
        perf_metrics = self.perf_tracker.get_metrics()
        cache_stats = self.cache.get_stats()
        
        return {
            "total_chunks": count,
            "embedding_dimension": self.embedding_gen.get_embedding_dimension(),
            "performance": perf_metrics,
            "cache": cache_stats
        }
    
    def get_all_documents(self) -> List[str]:
        results = self.vector_store.collection.get()
        if results and 'metadatas' in results:
            docs = set([meta['filename'] for meta in results['metadatas']])
            return list(docs)
        return []
    
    def clear_database(self):
        self.vector_store.clear_collection()
        self.cache.clear()
        self.perf_tracker.reset()
