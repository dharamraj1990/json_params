def validate_input(event):
    """
    Validate input event data
    """
    if not event:
        return False
    
    # Add your validation logic here
    if isinstance(event, dict):
        return True
    
    return False

