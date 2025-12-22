import os

def get_settings():
    """Get application settings"""
    return {
        'environment': os.environ.get('ENVIRONMENT', 'production'),
        'region': os.environ.get('AWS_REGION', 'us-east-1'),
        'version': '1.0.0',
        'features': {
            'logging': True,
            'validation': True
        }
    }

