# tests/test_model_selector.py
"""
Tests for Model Selector module
"""

import pytest
from unittest.mock import patch
from app.pipeline.model_selector import ModelSelector


class TestModelSelector:
    """Test suite for ModelSelector class."""
    
    def test_initialization(self):
        """Test ModelSelector initialization."""
        selector = ModelSelector(
            openai_api_key="test-key",
            google_api_key="test-key"
        )
        
        assert selector.openai_api_key == "test-key"
        assert selector.google_api_key == "test-key"
        assert selector.primary_model == "gpt-4o"
    
    def test_validate_api_keys(self):
        """Test API key validation."""
        selector = ModelSelector(
            openai_api_key="test-key",
            google_api_key=None
        )
        
        keys = selector.validate_api_keys()
        
        assert keys["openai"] is True
        assert keys["gemini"] is False
    
    def test_get_available_models(self):
        """Test getting available models."""
        selector = ModelSelector(
            openai_api_key="test-key",
            google_api_key="test-key"
        )
        
        models = selector.get_available_models()
        
        assert len(models) == 2
        assert any("OpenAI" in m for m in models)
        assert any("Gemini" in m for m in models)


# Run tests with: pytest tests/ -v