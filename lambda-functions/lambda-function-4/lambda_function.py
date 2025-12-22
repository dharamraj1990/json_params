import json
from datetime import datetime
from handlers.request_handler import RequestHandler
from handlers.response_handler import ResponseHandler
from config.settings import get_settings

def lambda_handler(event, context):
    """
    Lambda function handler with request/response handlers
    """
    settings = get_settings()
    
    # Initialize handlers
    request_handler = RequestHandler()
    response_handler = ResponseHandler()
    
    try:
        # Process request
        processed_data = request_handler.handle(event)
        
        # Generate response
        response_data = {
            'message': 'Request processed successfully',
            'function': 'lambda-function-4',
            'version': '1.0.1',
            'timestamp': datetime.utcnow().isoformat(),
            'data': processed_data,
            'settings': settings
        }
        
        return response_handler.create_response(200, response_data)
        
    except Exception as e:
        error_response = {
            'error': str(e),
            'function': 'lambda-function-4',
            'timestamp': datetime.utcnow().isoformat()
        }
        return response_handler.create_response(500, error_response)

