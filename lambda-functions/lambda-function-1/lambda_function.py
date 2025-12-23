import json
import os
from datetime import datetime

def lambda_handler(event, context):
    """
    Enhanced Lambda function handler with additional features
    
    Args:
        event: Lambda event data
        context: Lambda context object
    
    Returns:
        dict: Response with status code and body
    """
    # Log the incoming event
    print(f"Received event: {json.dumps(event)}")
    print(f"Function name: {context.function_name}")
    print(f"Request ID: {context.aws_request_id}")
    
    # Get environment variables if any
    env_vars = {
        'region': os.environ.get('AWS_REGION', 'us-east-1'),
        'function_version': context.function_version
    }
    
    # Process the event
    event_type = event.get('type', 'unknown')
    timestamp = datetime.utcnow().isoformat()
    
    # Enhanced response with more details
    response_data = {
        'message': 'Hello from Lambda!',
        'function': 'lambda-function-1',
        'version': '2.8.0',
        'timestamp': timestamp,
        'event_type': event_type,
        'environment': env_vars,
        'request_id': context.aws_request_id,
        'remaining_time_ms': context.get_remaining_time_in_millis(),
        'deployment': 'automated',
        'build_date': timestamp,
        'environment': 'dev',
        'last_updated': timestamp,
        'approval_required': True,
        'workflow_tested': True,
        'native_environment_protection': True,
        'event': event,
        'ci_cd_pipeline': 'github-actions',
        'deployment_status': 'success',
        'build_number': 'latest',
        'approval_method': 'github-issues',
        'approval_working': True,
        'branching_strategy': 'develop-release-only',
        'ecr_repo': 'stg-us-east-1-repo',
        'deployment_target': 'staging-and-production',
        'email_notifications': True
    }
    
    response = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'X-Function-Name': context.function_name
        },
        'body': json.dumps(response_data, indent=2)
    }
    
    return response
# Test comment
