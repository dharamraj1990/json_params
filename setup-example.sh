#!/bin/bash
# Setup script to create example Lambda function structure
# This script creates a sample lambda function folder structure

set -e

LAMBDA_DIR="lambda-functions"
SAMPLE_FUNCTION="lambda-function-1"

echo "Creating sample Lambda function structure..."

# Create lambda-functions directory if it doesn't exist
mkdir -p "$LAMBDA_DIR/$SAMPLE_FUNCTION"

# Create sample Dockerfile
cat > "$LAMBDA_DIR/$SAMPLE_FUNCTION/Dockerfile" << 'EOF'
FROM public.ecr.aws/lambda/python:3.11

WORKDIR ${LAMBDA_TASK_ROOT}

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy function code
COPY . .

# Set the CMD to your handler
CMD [ "lambda_function.lambda_handler" ]
EOF

# Create sample requirements.txt
cat > "$LAMBDA_DIR/$SAMPLE_FUNCTION/requirements.txt" << 'EOF'
# Add your Python dependencies here
# Example:
# requests==2.31.0
# boto3==1.28.0
EOF

# Create sample lambda_function.py
cat > "$LAMBDA_DIR/$SAMPLE_FUNCTION/lambda_function.py" << 'EOF'
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
            'function': 'lambda-function-1',
            'event': event
        })
    }
    
    return response
EOF

echo "✅ Sample Lambda function created at: $LAMBDA_DIR/$SAMPLE_FUNCTION"
echo ""
echo "Next steps:"
echo "1. Update .github/lambda-ecr-mapping.txt with your ECR repository names"
echo "2. Create ECR repositories in AWS"
echo "3. Configure AWS credentials in GitHub Secrets"
echo "4. Customize the Lambda function code as needed"
echo ""
echo "To create more Lambda functions, copy this structure:"
echo "  cp -r $LAMBDA_DIR/$SAMPLE_FUNCTION $LAMBDA_DIR/lambda-function-2"

