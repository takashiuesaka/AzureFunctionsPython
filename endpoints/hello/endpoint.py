"""
Hello World HTTP Function
Sample Azure Function demonstrating HTTP trigger with best practices.
"""
import azure.functions as func
import json
import logging
from datetime import datetime, timezone
from typing import Dict, Any

from shared.response_helpers import create_json_response
from shared.validators import validate_request_data


def hello_handler(req: func.HttpRequest) -> func.HttpResponse:
    """
    HTTP trigger function that returns a greeting message.
    
    Args:
        req: HTTP request object
        
    Returns:
        JSON response with greeting message
    """
    logging.info("Hello function processed a request.")
    
    try:
        # Get name from query params or request body
        name = req.params.get('name')
        
        if not name:
            try:
                req_body = req.get_json()
                if req_body:
                    name = req_body.get('name')
            except ValueError:
                pass
        
        # Validate input
        if name and not validate_request_data({'name': name}):
            return create_json_response(
                {"error": "Invalid input data"}, 
                status_code=400
            )
        
        # Create response data
        response_data: Dict[str, Any] = {
            "message": f"Hello, {name or 'World'}!",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "function": "hello",
            "version": "1.0.0"
        }
        
        logging.info(f"Hello function returning greeting for: {name or 'World'}")
        return create_json_response(response_data)
        
    except Exception as e:
        logging.error(f"Error in hello function: {str(e)}")
        return create_json_response(
            {"error": "Internal server error"}, 
            status_code=500
        )