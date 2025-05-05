import hashlib
import uuid
import base64
import os
import json
from datetime import datetime, timedelta

# Function to hash password
def hash_password(password):
    """
    Hash a password for storing
    """
    # In a real application, you would use a proper password hashing library like bcrypt
    # For simplicity, we'll use a basic SHA-256 hash with a salt
    salt = uuid.uuid4().hex
    hashed = hashlib.sha256(salt.encode() + password.encode()).hexdigest()
    return f"{salt}${hashed}"

# Function to verify password
def verify_password(password, hashed_password):
    """
    Verify a stored password against one provided by user
    """
    if not hashed_password or "$" not in hashed_password:
        return False
    
    salt, stored_hash = hashed_password.split("$", 1)
    calculated_hash = hashlib.sha256(salt.encode() + password.encode()).hexdigest()
    return calculated_hash == stored_hash

# Function to generate session ID
def generate_session_id():
    """
    Generate a unique session ID
    """
    return str(uuid.uuid4())

# Function to encrypt data
def encrypt_data(data, key):
    """
    Encrypt data using a key
    This is a simplified version for demonstration purposes
    In a real application, you would use a proper encryption library
    """
    # Convert data to JSON string
    data_str = json.dumps(data)
    
    # In a real application, you would use proper encryption
    # For simplicity, we'll use base64 encoding
    encoded = base64.b64encode(data_str.encode()).decode()
    
    return encoded

# Function to decrypt data
def decrypt_data(encrypted_data, key):
    """
    Decrypt data using a key
    This is a simplified version for demonstration purposes
    In a real application, you would use a proper encryption library
    """
    try:
        # In a real application, you would use proper decryption
        # For simplicity, we'll use base64 decoding
        decoded = base64.b64decode(encrypted_data.encode()).decode()
        
        # Convert JSON string back to data
        data = json.loads(decoded)
        
        return data
    except Exception as e:
        print(f"Error decrypting data: {e}")
        return None

# Function to validate input
def validate_input(input_str, input_type):
    """
    Validate input based on type
    Returns (is_valid, message)
    """
    if input_type == "email":
        # Simple email validation
        import re
        if not re.match(r"[^@]+@[^@]+\.[^@]+", input_str):
            return False, "Invalid email format"
    elif input_type == "phone":
        # Simple phone validation (10 digits)
        import re
        if not re.match(r"^[0-9]{10}$", input_str):
            return False, "Invalid phone number format (should be 10 digits)"
    elif input_type == "pan":
        # PAN validation (ABCDE1234F format)
        import re
        if not re.match(r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$", input_str):
            return False, "Invalid PAN format (should be ABCDE1234F)"
    elif input_type == "aadhar":
        # Aadhar validation (12 digits)
        import re
        if not re.match(r"^[0-9]{12}$", input_str):
            return False, "Invalid Aadhar format (should be 12 digits)"
    elif input_type == "amount":
        # Amount validation (positive number)
        try:
            amount = float(input_str)
            if amount <= 0:
                return False, "Amount must be positive"
        except ValueError:
            return False, "Invalid amount format"
    
    return True, "Valid input"

# Function to sanitize file path
def sanitize_file_path(path):
    """
    Sanitize file path to prevent directory traversal attacks
    """
    # Remove any path traversal attempts
    path = os.path.normpath(path)
    
    # Ensure the path doesn't go outside the allowed directory
    if os.path.isabs(path) or path.startswith(".."):
        return None
    
    return path

# Function to generate a secure token
def generate_token():
    """
    Generate a secure token for password reset, etc.
    """
    return uuid.uuid4().hex

# Function to validate token
def validate_token(token, expected_token, expiry=None):
    """
    Validate a token against an expected token with optional expiry
    """
    if not token or not expected_token:
        return False
    
    # Check if token matches
    if token != expected_token:
        return False
    
    # Check if token has expired
    if expiry and datetime.now() > expiry:
        return False
    
    return True
