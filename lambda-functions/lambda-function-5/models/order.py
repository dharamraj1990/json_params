class Order:
    """Order model"""
    
    def __init__(self, order_id, amount, items):
        self.id = order_id
        self.amount = amount
        self.items = items
    
    def get_total_items(self):
        """Get total number of items"""
        return len(self.items)
    
    def __repr__(self):
        return f"Order(id={self.id}, amount={self.amount}, items={self.get_total_items()})"

