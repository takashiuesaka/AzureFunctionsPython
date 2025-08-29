"""
Test configuration for Azure Functions
"""
import pytest
import sys
import os

# Add the parent directory to the path to import the function modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def mock_http_request():
    """
    Create a mock HTTP request for testing.
    """
    from unittest.mock import Mock
    import azure.functions as func
    
    def create_request(method="GET", url="http://localhost:7071/api/hello", 
                      params=None, json_body=None, headers=None):
        request = Mock(spec=func.HttpRequest)
        request.method = method
        request.url = url
        request.params = params or {}
        request.headers = headers or {}
        
        if json_body:
            request.get_json.return_value = json_body
        else:
            request.get_json.side_effect = ValueError("No JSON data")
        
        return request
    
    return create_request