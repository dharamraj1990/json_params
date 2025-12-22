class OrderService:
    """Service for processing orders"""
    
    def process_order(self, user, order):
        """Process an order"""
        return {
            'processed': True,
            'order_id': order.id,
            'user_id': user.id,
            'amount': order.amount,
            'item_count': order.get_total_items(),
            'status': 'completed'
        }

