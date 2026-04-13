import uuid

def get_contact_payload(overrides=None):
    """
    Returns a fresh dictionary for contact creation.
    Generates a unique email by default to avoid 'Email already exists' errors.
    """
    unique_id = str(uuid.uuid4())[:8]
    
    payload = {
        "user_name": f"User_{unique_id}",
        "email_address": f"test_{unique_id}@cypherware.com",
        "phone_number": "1234567890",
        "service_type": "QA Services",
        "project_name": "Automation Project",
        "project_description": "Default description"
    }
    
    if overrides:
        payload.update(overrides)
        
    return payload