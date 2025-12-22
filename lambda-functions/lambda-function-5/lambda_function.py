import json
from models.user import User
from models.order import Order
from services.order_service import OrderService
from services.notification_service import NotificationService

def lambda_handler(event, context):
    """
    Lambda function handler with business logic modules
    Handles order processing with user and order models
    """
    try:
        # Parse input
        user_data = event.get('user', {})
        order_data = event.get('order', {})
        
        # Create models
        user = User(user_data.get('id'), user_data.get('name'))
        order = Order(
            order_data.get('id'),
            order_data.get('amount'),
            order_data.get('items', [])
        )
        
        # Process order using service
        order_service = OrderService()
        result = order_service.process_order(user, order)
        
        # Send notification
        notification_service = NotificationService()
        notification_service.send_confirmation(user, order)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Order processed successfully',
                'function': 'lambda-function-5',
                'order_id': order.id,
                'user_id': user.id,
                'result': result
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'function': 'lambda-function-5'
            })
        }

