"""Streamlit version of Deep Research Agent for easy cloud deployment"""
import streamlit as st
import os
from modules.retriever import Retriever
from modules.reasoning import Reasoner

# Streamlit configuration
st.set_page_config(
    page_title="Deep Research Agent",
    page_icon="📚",
    layout="wide"
)

@st.cache_resource
def initialize_system():
    """Initialize the retriever and reasoner (cached)"""
    DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
    INDEX_DIR = os.path.join(os.path.dirname(__file__), "outputs", "index")
    os.makedirs(INDEX_DIR, exist_ok=True)
    
    retriever = Retriever(data_dir=DATA_DIR, index_dir=INDEX_DIR)
    retriever.build_or_load_index(force_rebuild=False)
    reasoner = Reasoner(retriever)
    return retriever, reasoner

def main():
    st.title("📚 Deep Research Agent")
    st.markdown("Ask questions about your documents and get AI-powered research insights!")
    
    # Initialize system
    try:
        with st.spinner("Initializing system..."):
            retriever, reasoner = initialize_system()
        
        # Check data files
        data_dir = os.path.join(os.path.dirname(__file__), "data")
        if os.path.exists(data_dir):
            data_files = len([f for f in os.listdir(data_dir) if f.endswith(('.txt', '.md', '.pdf'))])
            st.success(f"✅ System ready! Found {data_files} data files.")
        else:
            st.warning("⚠️ No data directory found. Please upload documents to the data/ folder.")
            return
        
        # Query input
        query = st.text_area(
            "Enter your research query:",
            placeholder="What would you like to research?",
            height=100
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            search_button = st.button("🔎 Search", type="primary")
        with col2:
            if st.button("🔄 Rebuild Index"):
                st.cache_resource.clear()
                st.rerun()
        
        if search_button and query.strip():
            with st.spinner("Processing your query..."):
                try:
                    # Run multi-step reasoning
                    combined, summary = reasoner.answer(query.strip())
                    
                    # Display results
                    st.markdown("## 📑 Retrieved Evidence")
                    with st.expander("View Retrieved Evidence", expanded=True):
                        st.text(combined)
                    
                    st.markdown("## 📝 Synthesized Summary")
                    with st.expander("View Summary", expanded=True):
                        st.text(summary)
                    
                    # Export option
                    export_path = os.path.join("outputs", "result.md")
                    reasoner.answer_and_export(query.strip(), export_path=export_path)
                    
                    if os.path.exists(export_path):
                        with open(export_path, 'r', encoding='utf-8') as f:
                            result_content = f.read()
                        
                        st.download_button(
                            label="📥 Download Result",
                            data=result_content,
                            file_name="research_result.md",
                            mime="text/markdown"
                        )
                    
                except Exception as e:
                    st.error(f"Error processing query: {str(e)}")
        
        elif search_button:
            st.warning("Please enter a query to search.")
            
    except Exception as e:
        st.error(f"Failed to initialize system: {str(e)}")
        st.info("Make sure all dependencies are installed and data files are available.")

if __name__ == "__main__":
    main()