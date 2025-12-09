import streamlit as st
import os
import time
from datetime import datetime
from src.rag_pipeline import RAGPipeline
from src.ner_processor import NERProcessor
from src.analytics import DocumentAnalytics
from src.report_generator import ReportGenerator
from config.config import MODELS, DATA_DIR, SUPPORTED_FORMATS

st.set_page_config(
    page_title="Document Intelligence Platform",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'rag_pipeline' not in st.session_state:
    st.session_state.rag_pipeline = RAGPipeline()
    st.session_state.ner_processor = NERProcessor()
    st.session_state.analytics = DocumentAnalytics()
    st.session_state.report_gen = ReportGenerator()
    st.session_state.chat_history = []
    st.session_state.uploaded_files = []
    st.session_state.current_model = "fast"
    st.session_state.processed_docs_data = []

def save_uploaded_file(uploaded_file):
    file_path = os.path.join(DATA_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

st.title("📚 Document Intelligence Platform")
st.markdown("### Enterprise AI-Powered Document Analysis")

with st.sidebar:
    st.header("⚙️ Configuration")
    
    model_choice = st.radio(
        "Select Model",
        options=["fast", "deep"],
        format_func=lambda x: MODELS[x]["display_name"],
        index=0 if st.session_state.current_model == "fast" else 1
    )
    
    if model_choice != st.session_state.current_model:
        st.session_state.current_model = model_choice
        st.session_state.rag_pipeline.set_model(MODELS[model_choice]["name"])
        st.success(f"✅ Switched to {MODELS[model_choice]['display_name']}")
    
    st.info(f"**Use Case:** {MODELS[model_choice]['use_case']}")
    
    st.markdown("---")
    
    st.header("📄 Document Management")
    
    uploaded_files = st.file_uploader(
        "Upload Documents",
        type=["pdf", "docx", "txt", "md"],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        if st.button("📤 Process Documents", type="primary", use_container_width=True):
            with st.spinner("Processing documents..."):
                file_paths = []
                for uploaded_file in uploaded_files:
                    file_path = save_uploaded_file(uploaded_file)
                    file_paths.append(file_path)
                
                result = st.session_state.rag_pipeline.ingest_documents(file_paths)
                st.session_state.uploaded_files.extend(result['documents'])
                st.session_state.processed_docs_data = result.get('processed_docs', [])
                
                st.success(f"✅ Processed {result['num_documents']} documents ({result['num_chunks']} chunks)")
    
    if st.session_state.uploaded_files:
        st.markdown("**📁 Uploaded Documents:**")
        for doc in set(st.session_state.uploaded_files):
            st.text(f"• {doc}")
    
    st.markdown("---")
    
    if st.button("🗑️ Clear Database", type="secondary", use_container_width=True):
        st.session_state.rag_pipeline.clear_database()
        st.session_state.chat_history = []
        st.session_state.uploaded_files = []
        st.session_state.processed_docs_data = []
        st.success("✅ Database cleared!")
        st.rerun()

tab1, tab2, tab3, tab4, tab5 = st.tabs(["💬 Q&A", "📊 Analytics", "🏷️ Entity Extraction", "🔍 Compare Docs", "📥 Export"])

with tab1:
    st.header("💬 Ask Questions")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        question = st.text_input(
            "Enter your question:",
            placeholder="What is this document about?",
            key="question_input"
        )
    
    with col2:
        use_cache = st.checkbox("Use Cache", value=True, help="Cache queries for faster responses")
    
    if st.button("🔍 Get Answer", type="primary") and question:
        if not st.session_state.uploaded_files:
            st.warning("⚠️ Please upload and process documents first!")
        else:
            with st.spinner("Generating answer..."):
                start_time = time.time()
                answer, sources, confidence = st.session_state.rag_pipeline.query(question, use_cache=use_cache)
                response_time = time.time() - start_time
                
                st.session_state.analytics.log_query(question, response_time, len(sources))
                
                st.session_state.chat_history.append({
                    "question": question,
                    "answer": answer,
                    "sources": sources,
                    "confidence": confidence,
                    "response_time": response_time,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
    
    if st.session_state.chat_history:
        st.markdown("---")
        st.subheader("📝 Conversation History")
        
        for i, chat in enumerate(reversed(st.session_state.chat_history)):
            with st.expander(f"Q: {chat['question']}", expanded=(i==0)):
                col_a, col_b, col_c = st.columns([2, 1, 1])
                with col_a:
                    confidence_color = "🟢" if chat['confidence']['level'] == "high" else "🟡" if chat['confidence']['level'] == "medium" else "🔴"
                    st.caption(f"{confidence_color} Confidence: {chat['confidence']['level'].upper()} ({chat['confidence']['score']:.2f})")
                with col_b:
                    st.caption(f"⏱️ {chat['response_time']:.2f}s")
                with col_c:
                    st.caption(f"🕐 {chat['timestamp']}")
                
                st.markdown(f"**Answer:**\n\n{chat['answer']}")
                
                st.markdown("**📚 Sources:**")
                for source in chat['sources']:
                    st.caption(f"[{source['source_number']}] **{source['filename']}** - {source['text']}")

with tab2:
    st.header("📊 Analytics Dashboard")
    
    stats = st.session_state.rag_pipeline.get_stats()
    analytics_data = st.session_state.analytics.get_analytics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📄 Total Chunks", stats['total_chunks'])
    with col2:
        st.metric("📁 Documents", len(set(st.session_state.uploaded_files)))
    with col3:
        st.metric("💬 Total Queries", analytics_data['total_queries'])
    with col4:
        if analytics_data['total_queries'] > 0:
            st.metric("⏱️ Avg Response Time", f"{analytics_data['avg_response_time']:.2f}s")
        else:
            st.metric("⏱️ Avg Response Time", "N/A")
    
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("🎯 Performance Metrics")
        if 'performance' in stats and stats['performance']:
            perf = stats['performance']
            for metric_name, metric_data in perf.items():
                if metric_data['count'] > 0:
                    st.write(f"**{metric_name.replace('_', ' ').title()}:**")
                    st.write(f"- Average: {metric_data['avg']:.3f}s")
                    st.write(f"- Min: {metric_data['min']:.3f}s | Max: {metric_data['max']:.3f}s")
                    st.write(f"- Count: {metric_data['count']}")
                    st.markdown("---")
        else:
            st.info("No performance data yet. Run some queries!")
    
    with col_right:
        st.subheader("💾 Cache Statistics")
        if 'cache' in stats:
            cache_stats = stats['cache']
            st.write(f"**Cache Size:** {cache_stats['cache_size']} / {cache_stats['max_size']}")
            st.progress(cache_stats['cache_size'] / cache_stats['max_size'])
        
        st.markdown("---")
        
        if analytics_data['total_queries'] > 0:
            st.subheader("📈 Recent Queries")
            for query in analytics_data['recent_queries'][-5:]:
                st.caption(f"• {query['query'][:50]}... ({query['response_time']:.2f}s)")

with tab3:
    st.header("🏷️ Named Entity Recognition")
    
    if st.session_state.processed_docs_data:
        selected_doc_for_ner = st.selectbox(
            "Select Document for Entity Extraction",
            options=[doc['filename'] for doc in st.session_state.processed_docs_data]
        )
        
        if st.button("🔍 Extract Entities", type="primary"):
            with st.spinner("Extracting entities..."):
                selected_doc_data = next((doc for doc in st.session_state.processed_docs_data if doc['filename'] == selected_doc_for_ner), None)
                
                if selected_doc_data:
                    entities = st.session_state.ner_processor.get_entity_summary(selected_doc_data['text'])
                    
                    if entities:
                        st.success(f"✅ Extracted entities from {selected_doc_for_ner}")
                        
                        for entity_type, data in entities.items():
                            with st.expander(f"{entity_type} ({data['count']} total, {data['unique']} unique)"):
                                for entity, count in data['most_common']:
                                    st.write(f"• **{entity}** - {count} occurrences")
                    else:
                        st.info("No entities found in this document")
    else:
        st.info("📤 Upload and process documents to extract entities")

with tab4:
    st.header("🔍 Multi-Document Comparison")
    
    all_docs = st.session_state.rag_pipeline.get_all_documents()
    
    if len(all_docs) >= 2:
        col1, col2 = st.columns(2)
        
        with col1:
            doc1 = st.selectbox("Select First Document", options=all_docs, key="doc1")
        
        with col2:
            doc2 = st.selectbox("Select Second Document", options=[d for d in all_docs if d != doc1], key="doc2")
        
        aspect = st.text_input("Comparison Aspect (optional)", placeholder="e.g., methodology, findings, conclusions")
        
        if st.button("🔄 Compare Documents", type="primary"):
            with st.spinner("Comparing documents..."):
                comparison = st.session_state.rag_pipeline.compare_documents(doc1, doc2, aspect or "general content")
                
                st.markdown("### 📊 Comparison Results")
                st.markdown(comparison)
    else:
        st.info("📤 Upload at least 2 documents to use comparison feature")

with tab5:
    st.header("📥 Export & Reports")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💬 Export Q&A Session")
        
        if st.session_state.chat_history:
            if st.button("📄 Generate PDF Report", type="primary", use_container_width=True):
                with st.spinner("Generating PDF report..."):
                    output_path = os.path.join(DATA_DIR, f"qa_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
                    st.session_state.report_gen.generate_qa_report(st.session_state.chat_history, output_path)
                    
                    with open(output_path, "rb") as f:
                        st.download_button(
                            label="⬇️ Download PDF Report",
                            data=f,
                            file_name=os.path.basename(output_path),
                            mime="application/pdf",
                            use_container_width=True
                        )
            
            if st.button("📋 Export as JSON", use_container_width=True):
                with st.spinner("Exporting to JSON..."):
                    output_path = os.path.join(DATA_DIR, f"qa_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
                    st.session_state.report_gen.export_to_json(st.session_state.chat_history, output_path)
                    
                    with open(output_path, "rb") as f:
                        st.download_button(
                            label="⬇️ Download JSON",
                            data=f,
                            file_name=os.path.basename(output_path),
                            mime="application/json",
                            use_container_width=True
                        )
        else:
            st.info("No conversation history to export. Ask some questions first!")
    
    with col2:
        st.subheader("📊 Export Analytics")
        
        if st.session_state.chat_history:
            if st.button("📈 Generate Analytics Report", type="primary", use_container_width=True):
                with st.spinner("Generating analytics report..."):
                    analytics_data = st.session_state.analytics.get_analytics()
                    
                    entities_data = {}
                    if st.session_state.processed_docs_data:
                        all_texts = [doc['text'] for doc in st.session_state.processed_docs_data]
                        entities_data = st.session_state.ner_processor.extract_from_multiple_docs(all_texts)
                    
                    output_path = os.path.join(DATA_DIR, f"analytics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
                    st.session_state.report_gen.generate_analytics_report(analytics_data, entities_data, output_path)
                    
                    with open(output_path, "rb") as f:
                        st.download_button(
                            label="⬇️ Download Analytics PDF",
                            data=f,
                            file_name=os.path.basename(output_path),
                            mime="application/pdf",
                            use_container_width=True
                        )
        else:
            st.info("No analytics data to export yet!")

st.markdown("---")
st.caption("🚀 Built with Streamlit, LangChain, ChromaDB, Ollama | 🔒 100% Local & Private")
