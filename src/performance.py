from functools import lru_cache
import hashlib
import time
from typing import Tuple, List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QueryCache:
    def __init__(self, max_size: int = 100):
        self.cache = {}
        self.max_size = max_size
        self.access_times = {}
    
    def _get_cache_key(self, query: str) -> str:
        return hashlib.md5(query.lower().encode()).hexdigest()
    
    def get(self, query: str) -> Tuple[str, List[Dict]] | None:
        key = self._get_cache_key(query)
        if key in self.cache:
            self.access_times[key] = time.time()
            logger.info(f"Cache hit for query: {query[:50]}")
            return self.cache[key]
        return None
    
    def set(self, query: str, result: Tuple[str, List[Dict]]):
        key = self._get_cache_key(query)
        
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.access_times, key=self.access_times.get)
            del self.cache[oldest_key]
            del self.access_times[oldest_key]
        
        self.cache[key] = result
        self.access_times[key] = time.time()
        logger.info(f"Cached result for query: {query[:50]}")
    
    def clear(self):
        self.cache.clear()
        self.access_times.clear()
        logger.info("Cache cleared")
    
    def get_stats(self) -> Dict:
        return {
            "cache_size": len(self.cache),
            "max_size": self.max_size,
            "hit_rate": "N/A"
        }

class PerformanceTracker:
    def __init__(self):
        self.metrics = {
            "query_times": [],
            "embedding_times": [],
            "retrieval_times": [],
            "generation_times": []
        }
    
    def track_query_time(self, duration: float):
        self.metrics["query_times"].append(duration)
    
    def track_embedding_time(self, duration: float):
        self.metrics["embedding_times"].append(duration)
    
    def track_retrieval_time(self, duration: float):
        self.metrics["retrieval_times"].append(duration)
    
    def track_generation_time(self, duration: float):
        self.metrics["generation_times"].append(duration)
    
    def get_metrics(self) -> Dict:
        import numpy as np
        
        result = {}
        for metric_name, values in self.metrics.items():
            if values:
                result[metric_name] = {
                    "avg": float(np.mean(values)),
                    "min": float(np.min(values)),
                    "max": float(np.max(values)),
                    "count": len(values)
                }
            else:
                result[metric_name] = {"avg": 0, "min": 0, "max": 0, "count": 0}
        
        return result
    
    def reset(self):
        for key in self.metrics:
            self.metrics[key] = []

def measure_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        logger.info(f"{func.__name__} took {duration:.2f}s")
        return result, duration
    return wrapper
