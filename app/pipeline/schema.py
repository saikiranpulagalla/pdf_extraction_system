"""
Schema Module
Defines Pydantic models for structured data validation.
"""

"""
Schema Module
Defines Pydantic models for structured data validation.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Dict, List, Any, Optional
import json


class ExtractedData(BaseModel):
    """
    Flexible schema for extracted data.
    This allows dynamic fields as the LLM auto-detects structure.
    """
    data: Dict[str, Any] = Field(
        description="Extracted structured data with flexible schema"
    )
    
    @field_validator('data')
    @classmethod
    def validate_data_structure(cls, v):
        """Ensure data is a valid dictionary."""
        if not isinstance(v, dict):
            raise ValueError("Data must be a dictionary")
        return v
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.data, indent=2, ensure_ascii=False)
    
    def to_dict(self) -> Dict[str, Any]:
        """Return the data dictionary."""
        return self.data


class ValidationResult(BaseModel):
    """Result of validation process."""
    is_valid: bool
    data: Optional[Dict[str, Any]] = None
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


def validate_json_structure(data: Any) -> ValidationResult:
    """
    Validate JSON structure from LLM output.
    
    Args:
        data: Data to validate (can be string or dict)
        
    Returns:
        ValidationResult with validation status and cleaned data
    """
    errors = []
    warnings = []
    
    # Handle string input (JSON string)
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError as e:
            # Try to extract JSON from markdown code blocks
            data = data.strip()
            if data.startswith("```"):
                # Remove markdown code blocks
                lines = data.split("\n")
                # Find start and end of JSON
                start_idx = 0
                for i, line in enumerate(lines):
                    if line.strip().startswith("```"):
                        start_idx = i + 1
                        break
                
                end_idx = len(lines)
                for i in range(len(lines) - 1, start_idx, -1):
                    if lines[i].strip().startswith("```"):
                        end_idx = i
                        break
                
                json_str = "\n".join(lines[start_idx:end_idx])
                try:
                    data = json.loads(json_str)
                except json.JSONDecodeError:
                    errors.append(f"Failed to parse JSON: {str(e)}")
                    return ValidationResult(is_valid=False, errors=errors, warnings=warnings)
            else:
                errors.append(f"Failed to parse JSON: {str(e)}")
                return ValidationResult(is_valid=False, errors=errors, warnings=warnings)
    
    # Validate it's a dictionary
    if not isinstance(data, dict):
        errors.append(f"Expected dictionary, got {type(data).__name__}")
        return ValidationResult(is_valid=False, errors=errors, warnings=warnings)
    
    # Check if data is empty
    if not data:
        errors.append("Extracted data is empty")
        return ValidationResult(is_valid=False, errors=errors, warnings=warnings)
    
    # Validate nested structures
    cleaned_data = _clean_data(data)
    
    # Check for common issues
    if len(cleaned_data) < 2:
        warnings.append("Data has very few sections. Extraction might be incomplete.")
    
    return ValidationResult(
        is_valid=True,
        data=cleaned_data,
        errors=errors,
        warnings=warnings
    )


def _clean_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clean and normalize data structure.
    
    Args:
        data: Raw data dictionary
        
    Returns:
        Cleaned data dictionary
    """
    if not isinstance(data, dict):
        return data
    
    cleaned = {}
    
    for key, value in data.items():
        # Clean key
        clean_key = key.strip()
        
        # Recursively clean nested structures
        if isinstance(value, dict):
            cleaned[clean_key] = _clean_data(value)
        elif isinstance(value, list):
            cleaned[clean_key] = [
                _clean_data(item) if isinstance(item, dict) else item
                for item in value
            ]
        elif isinstance(value, str):
            # Clean string values
            cleaned[clean_key] = value.strip() if value else value
        else:
            cleaned[clean_key] = value
    
    return cleaned


def merge_comments_column(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensure comments are properly integrated into the structure.
    
    Args:
        data: Data dictionary
        
    Returns:
        Data with comments properly structured
    """
    # This is a placeholder for future enhancement
    # The LLM already includes comments, but we can add
    # additional processing here if needed
    return data