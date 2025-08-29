"""
Hello endpoint blueprint
"""
import azure.functions as func
from .endpoint import hello_handler

# Create blueprint for hello endpoint
bp = func.Blueprint()

# Register HTTP trigger function
@bp.function_name(name="hello")
@bp.route(route="hello", methods=["GET", "POST"])
def hello(req: func.HttpRequest) -> func.HttpResponse:
    return hello_handler(req)