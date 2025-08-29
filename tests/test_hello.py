"""
Unit tests for hello endpoint
"""
import pytest
import json
from endpoints.hello.endpoint import hello_handler


class TestHelloEndpoint:
    """Test cases for hello endpoint"""
    
    def test_hello_with_query_param(self, mock_http_request):
        """Test hello function with name in query parameters"""
        request = mock_http_request(params={"name": "Azure"})
        
        response = hello_handler(request)
        
        assert response.status_code == 200
        response_data = json.loads(response.get_body())
        assert "Hello, Azure!" in response_data["message"]
        assert "timestamp" in response_data
        assert response_data["function"] == "hello"
        
    def test_hello_with_json_body(self, mock_http_request):
        """Test hello function with name in JSON body"""
        request = mock_http_request(
            method="POST",
            json_body={"name": "Functions"}
        )
        
        response = hello_handler(request)
        
        assert response.status_code == 200
        response_data = json.loads(response.get_body())
        assert "Hello, Functions!" in response_data["message"]
        
    def test_hello_without_name(self, mock_http_request):
        """Test hello function without name parameter"""
        request = mock_http_request()
        
        response = hello_handler(request)
        
        assert response.status_code == 200
        response_data = json.loads(response.get_body())
        assert "Hello, World!" in response_data["message"]
        
    def test_hello_with_invalid_name(self, mock_http_request):
        """Test hello function with invalid name"""
        request = mock_http_request(params={"name": "<script>alert('xss')</script>"})
        
        response = hello_handler(request)
        
        assert response.status_code == 400
        response_data = json.loads(response.get_body())
        assert "error" in response_data
        
    def test_hello_response_headers(self, mock_http_request):
        """Test response headers are properly set"""
        request = mock_http_request(params={"name": "Test"})
        
        response = hello_handler(request)
        
        assert response.headers["Content-Type"] == "application/json"
        assert "X-Content-Type-Options" in response.headers
        assert "X-Frame-Options" in response.headers