# tests/test_schema.py
"""
Tests for Schema validation module
"""

import pytest
from app.pipeline.schema import validate_json_structure, ValidationResult


class TestSchemaValidation:
    """Test suite for schema validation."""
    
    def test_validate_valid_dict(self):
        """Test validation with valid dictionary."""
        data = {"name": "John", "age": 30}
        result = validate_json_structure(data)
        
        assert result.is_valid
        assert result.data == data
        assert len(result.errors) == 0
    
    def test_validate_empty_dict(self):
        """Test validation with empty dictionary."""
        data = {}
        result = validate_json_structure(data)
        
        assert not result.is_valid
        assert "empty" in result.errors[0].lower()
    
    def test_validate_json_string(self):
        """Test validation with JSON string input."""
        data = '{"name": "John", "age": 30}'
        result = validate_json_structure(data)
        
        assert result.is_valid
        assert result.data["name"] == "John"
    
    def test_validate_invalid_json_string(self):
        """Test validation with invalid JSON string."""
        data = '{"name": "John", invalid}'
        result = validate_json_structure(data)
        
        assert not result.is_valid
        assert len(result.errors) > 0
