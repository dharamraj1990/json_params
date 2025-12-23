import json
from datetime import datetime

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
        'headers': {
            'Content-Type': 'application/json',
            'X-Function-Version': '3.0.0'
        },
        'body': json.dumps({
            'message': 'Hello from Lambda!',
            'function': 'lambda-function-2',
            'version': '3.0.0',
            'timestamp': datetime.utcnow().isoformat(),
            'deployment': 'automated',
            'build_date': datetime.utcnow().isoformat(),
            'environment': 'dev',
            'last_updated': datetime.utcnow().isoformat(),
            'approval_required': True,
            'workflow_tested': True,
            'native_environment_protection': True,
            'ci_cd_pipeline': 'github-actions',
            'deployment_status': 'success',
            'build_number': 'latest',
            'event': event
        })
    }
    
    return response
# Test comment
