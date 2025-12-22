class NotificationService:
    """Service for sending notifications"""
    
    def send_confirmation(self, user, order):
        """Send order confirmation notification"""
        # In a real implementation, this would send an email/SMS
        print(f"Notification sent to {user.name} for order {order.id}")
        return True

