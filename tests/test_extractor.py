"""
Tests for LLM Extractor module
"""

import pytest
from unittest.mock import Mock, patch
from app.pipeline.extractor import LLMExtractor
from app.pipeline.model_selector import ModelSelector


class TestLLMExtractor:
    """Test suite for LLMExtractor class."""
    
    @pytest.fixture
    def mock_model_selector(self):
        """Create a mock ModelSelector."""
        selector = Mock(spec=ModelSelector)
        selector.get_model_with_fallback.return_value = (Mock(), "openai")
        return selector
    
    def test_parse_json_valid(self, mock_model_selector):
        """Test JSON parsing with valid input."""
        extractor = LLMExtractor(mock_model_selector)
        
        json_str = '{"name": "John", "age": 30}'
        result = extractor._parse_json(json_str)
        
        assert result == {"name": "John", "age": 30}
    
    def test_parse_json_with_markdown(self, mock_model_selector):
        """Test JSON parsing with markdown code blocks."""
        extractor = LLMExtractor(mock_model_selector)
        
        json_str = '```json\n{"name": "John", "age": 30}\n```'
        result = extractor._parse_json(json_str)
        
        assert result == {"name": "John", "age": 30}
    
    def test_get_current_model_info(self, mock_model_selector):
        """Test getting current model information."""
        extractor = LLMExtractor(mock_model_selector)
        
        info = extractor.get_current_model_info()
        
        assert "model_type" in info
        assert "model_name" in info

