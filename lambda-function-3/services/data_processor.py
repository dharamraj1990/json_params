class DataProcessor:
    """Service class for processing data"""
    
    def __init__(self):
        self.processed_count = 0
    
    def process(self, data):
        """Process the input data"""
        self.processed_count += 1
        
        # Process data logic
        result = {
            'processed': True,
            'count': self.processed_count,
            'data_keys': list(data.keys()) if isinstance(data, dict) else []
        }
        
        return result

