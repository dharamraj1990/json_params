import json
from utils.logger import setup_logger
from utils.validator import validate_input
from services.data_processor import DataProcessor

logger = setup_logger(__name__)

def lambda_handler(event, context):
    """
    Lambda function handler with module structure
    Processes data using multiple imported modules
    """
    try:
        logger.info(f"Received event: {json.dumps(event)}")
        
        # Validate input
        if not validate_input(event):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid input data'})
            }
        
        # Process data using service module
        processor = DataProcessor()
        result = processor.process(event)
        
        logger.info(f"Processing completed: {result}")
        
        response = {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Data processed successfully',
                'function': 'lambda-function-3',
                'version': '1.1.0',
                'result': result,
                'request_id': context.aws_request_id
            })
        }
        return response
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

