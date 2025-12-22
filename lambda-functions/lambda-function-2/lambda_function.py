import json

def lambda_handler(event, context):
    """
    Sample Lambda function handler
    
    Args:
        event: Lambda event data
        context: Lambda context object
    
    Returns:
        dict: Response with status code and body
    """
    print(f"Received event: {json.dumps(event)}")
    
    # Your Lambda function logic here
    response = {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Hello from Lambda!',
            'function': 'lambda-function-2',
            'event': event
        })
    }
    
    return response
