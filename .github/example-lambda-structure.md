# Example Lambda Function Repository Structure

```
your-repo/
├── .github/
│   ├── workflows/
│   │   └── lambda-build-push.yml
│   └── lambda-ecr-mapping.txt
│   └── Dockerfile.template
├── lambda-functions/
│   ├── lambda-function-1/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── lambda_function.py
│   │   └── (other Python files)
│   ├── lambda-function-2/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── lambda_function.py
│   │   └── (other Python files)
│   ├── lambda-function-3/
│   │   └── ...
│   └── ... (up to lambda-function-10)
└── README.md
```

## Each Lambda Function Folder Should Contain:

1. **Dockerfile** - Docker configuration for the Lambda function
2. **requirements.txt** - Python dependencies
3. **lambda_function.py** - Main Lambda handler code
4. Any other Python modules or files needed

## Example lambda_function.py:

```python
import json

def lambda_handler(event, context):
    """
    Sample Lambda function handler
    """
    print(f"Received event: {json.dumps(event)}")
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Hello from Lambda!',
            'function': 'lambda-function-1'
        })
    }
```

## Example requirements.txt:

```
requests==2.31.0
boto3==1.28.0
```

