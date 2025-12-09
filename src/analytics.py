from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import numpy as np
from typing import List, Dict

class DocumentAnalytics:
    def __init__(self):
        self.query_history = []
        self.response_times = []
    
    def cluster_documents(self, embeddings: np.ndarray, n_clusters: int = 5) -> Dict:
        if len(embeddings) < n_clusters:
            n_clusters = max(2, len(embeddings) // 2)
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        labels = kmeans.fit_predict(embeddings)
        
        pca = PCA(n_components=2)
        embeddings_2d = pca.fit_transform(embeddings)
        
        return {
            "labels": labels.tolist(),
            "n_clusters": n_clusters,
            "embeddings_2d": embeddings_2d.tolist(),
            "cluster_sizes": [int(np.sum(labels == i)) for i in range(n_clusters)]
        }
    
    def log_query(self, query: str, response_time: float, num_sources: int):
        self.query_history.append({
            "query": query,
            "response_time": response_time,
            "num_sources": num_sources
        })
        self.response_times.append(response_time)
    
    def get_analytics(self) -> Dict:
        if not self.query_history:
            return {
                "total_queries": 0,
                "avg_response_time": 0,
                "query_patterns": []
            }
        
        return {
            "total_queries": len(self.query_history),
            "avg_response_time": np.mean(self.response_times),
            "min_response_time": np.min(self.response_times),
            "max_response_time": np.max(self.response_times),
            "recent_queries": self.query_history[-10:]
        }
    
    def get_query_suggestions(self, current_query: str, all_queries: List[str]) -> List[str]:
        suggestions = []
        current_lower = current_query.lower()
        
        for query in all_queries:
            if current_lower in query.lower() and query != current_query:
                suggestions.append(query)
        
        return suggestions[:5]
