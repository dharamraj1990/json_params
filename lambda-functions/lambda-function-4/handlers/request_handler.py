class RequestHandler:
    """Handles incoming requests"""
    
    def handle(self, event):
        """Process the incoming event"""
        processed = {
            'event_type': type(event).__name__,
            'has_data': bool(event),
            'processed_at': self._get_timestamp()
        }
        
        if isinstance(event, dict):
            processed['keys'] = list(event.keys())
            processed['data'] = event
        
        return processed
    
    def _get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.utcnow().isoformat()

