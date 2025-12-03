"""
Tests for PDF Loader module
"""

import pytest
from io import BytesIO
from app.pipeline.pdf_loader import PDFLoader


class TestPDFLoader:
    """Test suite for PDFLoader class."""
    
    def test_initialization(self):
        """Test PDFLoader initialization."""
        loader = PDFLoader()
        assert loader.max_pages == 2
    
    def test_clean_text(self):
        """Test text cleaning functionality."""
        loader = PDFLoader()
        
        # Test excessive whitespace removal
        dirty_text = "Hello    World\n\n\n\nTest"
        clean_text = loader._clean_text(dirty_text)
        assert "    " not in clean_text
        assert "\n\n\n" not in clean_text
    
    def test_validate_pdf_invalid_empty(self):
        """Test PDF validation with empty bytes."""
        loader = PDFLoader()
        is_valid, error = loader.validate_pdf(b"")
        assert not is_valid
        assert error is not None
