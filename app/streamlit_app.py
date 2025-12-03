"""
Main Streamlit Application
AI-Powered PDF Extraction System with Excel Export
"""

import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv
import json
import traceback

from pipeline.pdf_loader import PDFLoader
from pipeline.model_selector import ModelSelector
from pipeline.extractor import LLMExtractor
from pipeline.excel_writer import ExcelWriter

# Load environment variables
load_dotenv()


def initialize_session_state():
    """Initialize Streamlit session state."""
    if 'extraction_complete' not in st.session_state:
        st.session_state.extraction_complete = False
    if 'extracted_data' not in st.session_state:
        st.session_state.extracted_data = None
    if 'excel_buffer' not in st.session_state:
        st.session_state.excel_buffer = None
    if 'pdf_text' not in st.session_state:
        st.session_state.pdf_text = None


def main():
    """Main application function."""
    
    # Page configuration
    st.set_page_config(
        page_title="AI PDF Extraction System",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    initialize_session_state()
    
    # Header
    st.title("📄 AI-Powered PDF Data Extraction")
    st.markdown("""
    Extract structured data from PDFs using advanced AI models (OpenAI GPT-4o / Google Gemini).
    Upload a 1-2 page PDF and download the extracted data in Excel format.
    """)
    
    # Sidebar - Configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Keys
        st.subheader("API Keys")
        openai_key = st.text_input(
            "OpenAI API Key",
            value=os.getenv("OPENAI_API_KEY", ""),
            type="password",
            help="Primary extraction model"
        )
        
        google_key = st.text_input(
            "Google API Key",
            value=os.getenv("GOOGLE_API_KEY", ""),
            type="password",
            help="Fallback extraction model"
        )
        
        # Model Selection
        st.subheader("Model Settings")
        primary_model = st.selectbox(
            "Primary Model (OpenAI)",
            ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"],
            index=0
        )
        
        fallback_model = st.selectbox(
            "Fallback Model (Gemini)",
            ["gemini-2.5-flash", "gemini-1.5-pro"],
            index=0
        )
        
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.1,
            step=0.1,
            help="Lower = more focused, Higher = more creative"
        )
        
        # Validate API keys
        st.divider()
        if openai_key or google_key:
            st.success("✅ At least one API key configured")
        else:
            st.error("❌ No API keys configured")
            st.info("Set API keys in .env file or enter them above")
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📤 Upload PDF")
        
        uploaded_file = st.file_uploader(
            "Choose a PDF file (1-2 pages)",
            type=['pdf'],
            help="Upload a PDF document to extract structured data"
        )
        
        if uploaded_file is not None:
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            st.info(f"File size: {uploaded_file.size / 1024:.2f} KB")
            
            # Process button
            if st.button("🚀 Extract Data", type="primary", use_container_width=True):
                if not openai_key and not google_key:
                    st.error("❌ Please provide at least one API key")
                else:
                    extract_data(
                        uploaded_file,
                        openai_key,
                        google_key,
                        primary_model,
                        fallback_model,
                        temperature
                    )
    
    with col2:
        st.header("📊 Results")
        
        if st.session_state.extraction_complete and st.session_state.extracted_data:
            st.success("✅ Extraction completed successfully!")
            
            # Display extracted data
            with st.expander("📋 View Extracted JSON", expanded=True):
                st.json(st.session_state.extracted_data)
            
            # Download button
            if st.session_state.excel_buffer:
                st.download_button(
                    label="📥 Download Excel File",
                    data=st.session_state.excel_buffer,
                    file_name="extracted_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    type="primary",
                    use_container_width=True
                )
            
            # Show extracted text
            if st.session_state.pdf_text:
                with st.expander("📄 View Extracted Text"):
                    st.text_area(
                        "Raw PDF Text",
                        value=st.session_state.pdf_text,
                        height=300,
                        disabled=True
                    )
        else:
            st.info("👆 Upload a PDF and click 'Extract Data' to begin")
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p><strong>AI PDF Extraction System</strong> | Powered by LangChain, OpenAI & Google Gemini</p>
        <p style='font-size: 0.9em;'>100% Content Extraction | Zero Hardcoded Keys | Automatic Fallback</p>
    </div>
    """, unsafe_allow_html=True)


def extract_data(
    uploaded_file,
    openai_key: str,
    google_key: str,
    primary_model: str,
    fallback_model: str,
    temperature: float
):
    """
    Extract data from uploaded PDF.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        openai_key: OpenAI API key
        google_key: Google API key
        primary_model: Primary model name
        fallback_model: Fallback model name
        temperature: Model temperature
    """
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Load PDF
        status_text.text("📄 Loading PDF...")
        progress_bar.progress(10)
        
        pdf_loader = PDFLoader()
        pdf_bytes = uploaded_file.read()
        
        # Validate PDF
        is_valid, error_msg = pdf_loader.validate_pdf(pdf_bytes)
        if not is_valid:
            st.error(f"❌ PDF Validation Failed: {error_msg}")
            progress_bar.empty()
            status_text.empty()
            return
        
        # Extract text
        status_text.text("📝 Extracting text from PDF...")
        progress_bar.progress(25)
        
        pdf_text = pdf_loader.load_from_bytes(pdf_bytes)
        st.session_state.pdf_text = pdf_text
        
        # Step 2: Initialize models
        status_text.text("🤖 Initializing AI models...")
        progress_bar.progress(40)
        
        model_selector = ModelSelector(
            openai_api_key=openai_key if openai_key else None,
            google_api_key=google_key if google_key else None,
            primary_model=primary_model,
            fallback_model=fallback_model,
            temperature=temperature
        )
        
        # Check available models
        available = model_selector.get_available_models()
        st.info(f"🔧 Available models: {', '.join(available)}")
        
        # Step 3: Extract data
        status_text.text("🧠 Extracting structured data with AI...")
        progress_bar.progress(55)
        
        extractor = LLMExtractor(model_selector)
        extracted_data = extractor.extract(pdf_text)
        
        model_info = extractor.get_current_model_info()
        st.info(f"✅ Used model: {model_info['model_type'].upper()} - {model_info['model_name']}")
        
        # Store in session state
        st.session_state.extracted_data = extracted_data
        
        # Step 4: Convert to Excel
        status_text.text("📊 Converting to Excel format...")
        progress_bar.progress(80)
        
        excel_writer = ExcelWriter()
        excel_buffer = excel_writer.json_to_excel(extracted_data)
        
        # Store in session state
        st.session_state.excel_buffer = excel_buffer
        
        # Complete
        progress_bar.progress(100)
        status_text.text("✅ Extraction complete!")
        st.session_state.extraction_complete = True
        
        # Clear progress indicators after a moment
        import time
        time.sleep(1)
        progress_bar.empty()
        status_text.empty()
        
        # Trigger rerun to show results
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ Extraction failed: {str(e)}")
        st.error("**Detailed Error:**")
        st.code(traceback.format_exc())
        progress_bar.empty()
        status_text.empty()


if __name__ == "__main__":
    main()