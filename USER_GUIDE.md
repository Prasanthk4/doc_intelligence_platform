# Document Intelligence Platform - User Guide

## 🚀 Quick Start

### 1. Start the Application

```bash
cd d:\ML\document-intelligence-platform
streamlit run app.py
```

The app will open in your browser at: **http://localhost:8501**

### 2. Upload Documents

1. Look at the **sidebar** on the left
2. Click **"Browse files"** under "Upload Documents"
3. Select one or more documents (PDF, DOCX, TXT, MD)
4. Click **"Process Documents"** button
5. Wait for success message showing number of chunks processed

### 3. Ask Questions

1. In the main area, find **"Enter your question"** text box
2. Type your question in natural language
3. Click **"Get Answer"** button
4. View the answer with source citations below

### 4. View Conversation History

- All your questions and answers are saved in **"Conversation History"**
- Click on any question to expand and see the full answer
- Sources are shown with document name and text excerpts

### 5. Switch Models (Optional)

In the sidebar:
- **Fast Mode (Llama 3.2 3B)**: Quick responses, good for simple questions
- **Deep Analysis (Mistral 7B)**: Slower but more accurate for complex questions

### 6. Generate Document Summary

1. In the right panel, select a document from the dropdown
2. Click **"Generate Summary"**
3. View the AI-generated summary below

### 7. View Statistics

The right panel shows:
- **Total Chunks**: Number of document chunks in database
- **Embedding Dimension**: Vector size (384)
- **Documents Loaded**: Number of documents processed

### 8. Clear Database

To start fresh:
1. Click **"Clear Database"** in the sidebar
2. All documents and conversation history will be removed

---

## 💡 Tips for Best Results

### Writing Good Questions

✅ **Good**: "What is the main topic of this document?"  
✅ **Good**: "Who are the authors mentioned?"  
✅ **Good**: "What are the key findings in section 3?"  

❌ **Avoid**: Very vague questions like "Tell me everything"  
❌ **Avoid**: Questions about information not in the documents  

### Document Preparation

- **PDF**: Works best with text-based PDFs (not scanned images)
- **DOCX**: Standard Word documents work perfectly
- **TXT/MD**: Plain text files are fastest to process

### Performance

- **First query**: May take 5-7 seconds (model loading)
- **Subsequent queries**: 2-3 seconds
- **Large documents**: Processing may take 10-20 seconds

---

## 🔧 Troubleshooting

### App Won't Start

**Error**: `ModuleNotFoundError`
- **Solution**: Run `pip install -r requirements.txt`

**Error**: `ollama: command not found`
- **Solution**: Install Ollama from https://ollama.ai/download

### No Answer Generated

**Issue**: Answer says "I cannot find this information"
- **Cause**: Information not in uploaded documents
- **Solution**: Upload relevant documents or rephrase question

### Slow Responses

**Issue**: Queries taking >10 seconds
- **Cause**: Large documents or complex questions
- **Solution**: Switch to "Fast Mode" (Llama 3.2 3B)

---

## 📚 Example Use Cases

### 1. Research Paper Analysis
- Upload multiple research papers
- Ask: "What are the common methodologies used?"
- Compare findings across papers

### 2. Policy Document Review
- Upload company policies
- Ask: "What is the remote work policy?"
- Get instant answers with page references

### 3. Contract Analysis
- Upload contracts
- Ask: "What are the payment terms?"
- Find specific clauses quickly

### 4. Study Material
- Upload textbooks or notes
- Ask questions to test understanding
- Get summaries of chapters

---

## 🎯 Advanced Features (Coming Soon)

The following features are coded but not yet integrated into the UI:

- **Named Entity Recognition**: Extract people, organizations, dates
- **Document Comparison**: Compare multiple documents side-by-side
- **Export Reports**: Generate PDF reports of Q&A sessions
- **Analytics Dashboard**: Query patterns and usage metrics
- **Confidence Scoring**: See how confident the AI is in answers

---

## 📞 Support

For issues or questions:
1. Check the `README.md` file
2. Review the `OLLAMA_SETUP.md` for installation help
3. Check the `walkthrough.md` for technical details

---

## 🔒 Privacy & Security

- **All processing is local**: No data sent to external servers
- **Ollama runs locally**: Your documents never leave your machine
- **No API keys needed**: Completely free and private
- **Data storage**: Documents stored in `d:\ML\document-intelligence-platform\data`
