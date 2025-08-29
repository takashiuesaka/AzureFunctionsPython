import azure.functions as func
import logging

# Import blueprints from endpoints
from endpoints.hello import bp as hello_bp

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create the main function app
app = func.FunctionApp()

# Register blueprints
app.register_blueprint(hello_bp)