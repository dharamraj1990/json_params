import json

class ResponseHandler:
    """Handles response creation"""
    
    def create_response(self, status_code, data):
        """Create a standardized response"""
        return {
            'statusCode': status_code,
            'headers': {
                'Content-Type': 'application/json',
                'X-Processed-By': 'lambda-function-4'
            },
            'body': json.dumps(data, indent=2)
        }

