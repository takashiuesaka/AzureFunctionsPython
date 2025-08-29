"""
Unit tests for shared utilities
"""
import pytest
from shared.validators import validate_name, validate_request_data, sanitize_string
from shared.response_helpers import create_json_response, create_error_response


class TestValidators:
    """Test cases for validation utilities"""
    
    def test_validate_name_valid(self):
        """Test name validation with valid names"""
        assert validate_name("John") is True
        assert validate_name("John Doe") is True
        assert validate_name("John-Doe") is True
        assert validate_name("John_Doe") is True
        assert validate_name("John123") is True
        
    def test_validate_name_invalid(self):
        """Test name validation with invalid names"""
        assert validate_name("") is False
        assert validate_name("   ") is False
        assert validate_name("a" * 101) is False  # Too long
        assert validate_name("<script>") is False
        assert validate_name("John@Doe") is False
        assert validate_name(123) is False  # Not a string
        
    def test_validate_request_data(self):
        """Test request data validation"""
        assert validate_request_data({"name": "John"}) is True
        assert validate_request_data({"other": "value"}) is True
        assert validate_request_data({"name": "<script>"}) is False
        assert validate_request_data("not a dict") is False
        
    def test_sanitize_string(self):
        """Test string sanitization"""
        assert sanitize_string("Hello World") == "Hello World"
        assert sanitize_string("  Hello World  ") == "Hello World"
        assert sanitize_string("Hello\x00World") == "HelloWorld"
        assert sanitize_string("a" * 300, 10) == "a" * 10
        assert sanitize_string(123) == ""


class TestResponseHelpers:
    """Test cases for response helper utilities"""
    
    def test_create_json_response(self):
        """Test JSON response creation"""
        data = {"message": "test"}
        response = create_json_response(data)
        
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        assert "X-Content-Type-Options" in response.headers
        
    def test_create_json_response_with_custom_status(self):
        """Test JSON response with custom status code"""
        data = {"message": "created"}
        response = create_json_response(data, status_code=201)
        
        assert response.status_code == 201
        
    def test_create_error_response(self):
        """Test error response creation"""
        response = create_error_response("Test error", 400, "TEST_ERROR")
        
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"