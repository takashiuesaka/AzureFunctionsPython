"""
Shared response helpers for Azure Functions
"""
import azure.functions as func
import json
from typing import Dict, Any, Optional


def create_json_response(
    data: Dict[str, Any], 
    status_code: int = 200,
    headers: Optional[Dict[str, str]] = None
) -> func.HttpResponse:
    """
    Create a JSON HTTP response with proper headers.
    
    Args:
        data: Dictionary to serialize as JSON
        status_code: HTTP status code (default: 200)
        headers: Additional headers (optional)
        
    Returns:
        HttpResponse object with JSON content
    """
    response_headers = {
        "Content-Type": "application/json",
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY"
    }
    
    if headers:
        response_headers.update(headers)
    
    return func.HttpResponse(
        body=json.dumps(data, ensure_ascii=False),
        status_code=status_code,
        headers=response_headers
    )


def create_error_response(
    message: str, 
    status_code: int = 500,
    error_code: Optional[str] = None
) -> func.HttpResponse:
    """
    Create a standardized error response.
    
    Args:
        message: Error message
        status_code: HTTP status code
        error_code: Optional error code for client handling
        
    Returns:
        HttpResponse object with error details
    """
    error_data = {
        "error": {
            "message": message,
            "status_code": status_code
        }
    }
    
    if error_code:
        error_data["error"]["code"] = error_code
    
    return create_json_response(error_data, status_code)