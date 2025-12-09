import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
CHROMA_DIR = os.path.join(DATA_DIR, "chroma_db")

MODELS = {
    "fast": {
        "name": "llama3.2:3b",
        "display_name": "Fast Mode (Llama 3.2 3B)",
        "description": "Quick responses, good accuracy",
        "use_case": "General Q&A, simple queries"
    },
    "deep": {
        "name": "mistral:7b",
        "display_name": "Deep Analysis (Mistral 7B)",
        "description": "Slower but more accurate",
        "use_case": "Complex analysis, multi-document comparison"
    }
}

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

SUPPORTED_FORMATS = [".pdf", ".docx", ".txt", ".md"]

RETRIEVAL_TOP_K = 5

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(CHROMA_DIR, exist_ok=True)
