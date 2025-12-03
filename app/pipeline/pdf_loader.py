"""
PDF Loader Module
Extracts text from PDF files using pdfplumber with formatting preservation.
"""

import pdfplumber
import re
from typing import Optional
from io import BytesIO


class PDFLoader:
    """Loads and extracts text from PDF files."""
    
    def __init__(self):
        self.max_pages = 2  # Limit to 1-2 pages as per requirements
    
    def load_from_bytes(self, pdf_bytes: bytes) -> str:
        """
        Load PDF from bytes and extract text.
        
        Args:
            pdf_bytes: PDF file as bytes
            
        Returns:
            Extracted and cleaned text
        """
        try:
            with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
                return self._extract_text(pdf)
        except Exception as e:
            raise Exception(f"Failed to load PDF: {str(e)}")
    
    def load_from_path(self, pdf_path: str) -> str:
        """
        Load PDF from file path and extract text.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted and cleaned text
        """
        try:
            with pdfplumber.open(pdf_path) as pdf:
                return self._extract_text(pdf)
        except Exception as e:
            raise Exception(f"Failed to load PDF from path: {str(e)}")
    
    def _extract_text(self, pdf) -> str:
        """
        Extract text from PDF pages.
        
        Args:
            pdf: pdfplumber PDF object
            
        Returns:
            Cleaned and formatted text
        """
        if len(pdf.pages) == 0:
            raise Exception("PDF has no pages")
        
        # Extract text from first 1-2 pages
        pages_to_process = min(len(pdf.pages), self.max_pages)
        text_parts = []
        
        for i in range(pages_to_process):
            page = pdf.pages[i]
            page_text = page.extract_text()
            
            if page_text:
                text_parts.append(page_text)
        
        full_text = "\n\n".join(text_parts)
        
        # Clean the text
        cleaned_text = self._clean_text(full_text)
        
        if not cleaned_text.strip():
            raise Exception("No text could be extracted from PDF")
        
        return cleaned_text
    
    def _clean_text(self, text: str) -> str:
        """
        Clean extracted text while preserving important formatting.
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        # Remove excessive whitespace but preserve line breaks
        text = re.sub(r' +', ' ', text)
        
        # Remove more than 2 consecutive newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Remove leading/trailing whitespace from each line
        lines = [line.strip() for line in text.split('\n')]
        text = '\n'.join(lines)
        
        # Remove any remaining multiple spaces
        text = re.sub(r'  +', ' ', text)
        
        return text.strip()
    
    def validate_pdf(self, pdf_bytes: bytes) -> tuple[bool, Optional[str]]:
        """
        Validate if PDF can be processed.
        
        Args:
            pdf_bytes: PDF file as bytes
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
                if len(pdf.pages) == 0:
                    return False, "PDF has no pages"
                
                if len(pdf.pages) > self.max_pages:
                    return False, f"PDF has {len(pdf.pages)} pages. Maximum allowed is {self.max_pages}"
                
                # Try to extract text from first page
                page_text = pdf.pages[0].extract_text()
                if not page_text or not page_text.strip():
                    return False, "PDF appears to be empty or contains only images"
                
                return True, None
        except Exception as e:
            return False, f"PDF validation failed: {str(e)}"