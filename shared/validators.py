"""
Request validation utilities
"""
import re
from typing import Dict, Any, List, Optional


def validate_request_data(data: Dict[str, Any]) -> bool:
    """
    Basic validation for request data.
    
    Args:
        data: Dictionary containing request data
        
    Returns:
        True if data is valid, False otherwise
    """
    if not isinstance(data, dict):
        return False
    
    # Check for required fields based on data content
    if 'name' in data:
        return validate_name(data['name'])
    
    return True


def validate_name(name: str) -> bool:
    """
    Validate name field.
    
    Args:
        name: Name string to validate
        
    Returns:
        True if name is valid, False otherwise
    """
    if not isinstance(name, str):
        return False
    
    # Basic validation: only letters, spaces, and common punctuation
    # Length between 1 and 100 characters
    if not (1 <= len(name.strip()) <= 100):
        return False
    
    # Allow letters, numbers, spaces, and basic punctuation
    pattern = r'^[a-zA-Z0-9\s\.\-\_]+$'
    return bool(re.match(pattern, name.strip()))


def sanitize_string(value: str, max_length: int = 255) -> str:
    """
    Sanitize string input.
    
    Args:
        value: String to sanitize
        max_length: Maximum allowed length
        
    Returns:
        Sanitized string
    """
    if not isinstance(value, str):
        return ""
    
    # Remove control characters and trim
    sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', value.strip())
    
    # Truncate if too long
    return sanitized[:max_length] if len(sanitized) > max_length else sanitized