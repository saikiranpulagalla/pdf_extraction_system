"""
Tests for Excel Writer module
"""

import pytest
from app.pipeline.excel_writer import ExcelWriter


class TestExcelWriter:
    """Test suite for ExcelWriter class."""
    
    def test_initialization(self):
        """Test ExcelWriter initialization."""
        writer = ExcelWriter()
        assert writer.header_fill is not None
        assert writer.header_font is not None
    
    def test_format_value_list(self):
        """Test value formatting for lists."""
        writer = ExcelWriter()
        
        value = ["Python", "Java", "JavaScript"]
        formatted = writer._format_value(value)
        
        assert formatted == "Python, Java, JavaScript"
    
    def test_format_value_dict(self):
        """Test value formatting for dictionaries."""
        writer = ExcelWriter()
        
        value = {"skill": "Python", "level": "Expert"}
        formatted = writer._format_value(value)
        
        assert "skill: Python" in formatted
        assert "level: Expert" in formatted
    
    def test_json_to_excel_basic(self):
        """Test basic JSON to Excel conversion."""
        writer = ExcelWriter()
        
        data = {
            "Basic Details": {
                "name": "John Doe",
                "email": "john@example.com"
            }
        }
        
        excel_buffer = writer.json_to_excel(data)
        
        assert excel_buffer is not None
        assert excel_buffer.getvalue()  # Check buffer has content
