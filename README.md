# 📚 Document Intelligence Platform

AI-powered document analysis system using RAG (Retrieval-Augmented Generation) with local LLMs.

## Features

- **Multi-format Support**: PDF, DOCX, TXT, Markdown
- **Intelligent Q&A**: Ask questions and get accurate answers with source citations
- **Document Summarization**: Automatic summary generation
- **Dual Model Support**: Fast mode (Llama 3.2 3B) and Deep Analysis (Mistral 7B)
- **Conversation History**: Track all Q&A sessions
- **Semantic Search**: Vector-based similarity search
- **Privacy-First**: All processing happens locally

## Tech Stack

- **LLM**: Ollama (Llama 3.2 / Mistral)
- **Embeddings**: Sentence Transformers
- **Vector DB**: ChromaDB
- **Framework**: LangChain
- **UI**: Streamlit
- **Document Processing**: PyPDF2, python-docx

## Installation

### Prerequisites

1. Install Ollama from https://ollama.ai
2. Pull required models:
```bash
ollama pull llama3.2:3b
ollama pull mistral:7b
```

### Setup

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Upload documents using the sidebar
3. Click "Process Documents"
4. Ask questions in the main interface
5. View answers with source citations

## Project Structure

```
document-intelligence-platform/
├── app.py                      # Main Streamlit application
├── src/
│   ├── document_processor.py  # Document parsing and chunking
│   ├── embeddings.py           # Embedding generation
│   ├── vector_store.py         # ChromaDB operations
│   ├── llm_handler.py          # Ollama integration
│   └── rag_pipeline.py         # RAG orchestration
├── config/
│   └── config.py               # Configuration settings
├── data/                       # Document storage
└── requirements.txt
```

## How It Works

1. **Document Processing**: Extracts text from uploaded files and splits into chunks
2. **Embedding Generation**: Converts text chunks to vector embeddings
3. **Vector Storage**: Stores embeddings in ChromaDB for fast retrieval
4. **Query Processing**: Converts questions to embeddings and finds similar chunks
5. **Answer Generation**: LLM generates answers based on retrieved context

## Model Selection

- **Fast Mode (Llama 3.2 3B)**: Quick responses, suitable for general queries
- **Deep Analysis (Mistral 7B)**: More accurate, better for complex questions

## ML Components

- **Neural Networks**: Transformer-based embedding models
- **Vector Similarity**: Cosine similarity for semantic search
- **LLM**: 3B/7B parameter language models
- **RAG Pipeline**: Production ML system combining retrieval and generation
