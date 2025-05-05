import os
import json
import glob
import uuid
import shutil
import tempfile
from datetime import datetime

# Base directory for data
DATA_DIR = "data"
USERS_DIR = os.path.join(DATA_DIR, "users")

# Ensure directories exist
os.makedirs(USERS_DIR, exist_ok=True)

# Function to load user data
def load_user_data(user_id):
    """
    Load user data from JSON file
    Returns user data dictionary or None if not found
    """
    if not user_id:
        return None
    
    file_path = os.path.join(USERS_DIR, f"{user_id}.json")
    
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
        return None
    except Exception as e:
        print(f"Error loading user data: {e}")
        return None

# Function to save user data
def save_user_data(user_data):
    """
    Save user data to JSON file
    Returns (success, message) tuple
    """
    if not user_data or "user_id" not in user_data:
        return False, "Invalid user data"
    
    user_id = user_data["user_id"]
    file_path = os.path.join(USERS_DIR, f"{user_id}.json")
    
    # Use atomic write to prevent data corruption
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            # Write data to temporary file
            json.dump(user_data, temp_file, indent=4)
        
        # Replace the original file with the temporary file
        shutil.move(temp_file.name, file_path)
        
        return True, "User data saved successfully"
    except Exception as e:
        # Clean up temporary file if it exists
        if 'temp_file' in locals():
            try:
                os.unlink(temp_file.name)
            except:
                pass
        
        print(f"Error saving user data: {e}")
        return False, f"Error saving user data: {str(e)}"

# Function to get all users
def get_all_users():
    """
    Get all users from the users.json file.
    Returns a dictionary of users.
    """
    DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    USERS_FILE = os.path.join(DATA_DIR, 'users.json')
    
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Function to perform atomic transaction
def atomic_transaction(user_id, transaction_func, *args, **kwargs):
    """
    Perform an atomic transaction on user data
    transaction_func should be a function that takes user_data as first argument
    and returns (success, modified_user_data, message)
    
    Returns (success, message) tuple
    """
    if not user_id:
        return False, "Invalid user ID"
    
    # Load user data
    user_data = load_user_data(user_id)
    
    if not user_data:
        return False, "User not found"
    
    # Perform transaction
    success, modified_user_data, message = transaction_func(user_data, *args, **kwargs)
    
    if not success:
        return False, message
    
    # Save modified user data
    save_success, save_message = save_user_data(modified_user_data)
    
    if not save_success:
        return False, save_message
    
    return True, message

# Function to add transaction
def add_transaction(user_id, account_index, transaction_type, amount, description):
    """
    Add a transaction to user account
    Returns (success, message) tuple
    """
    def transaction_func(user_data):
        if "accounts" not in user_data or account_index >= len(user_data["accounts"]):
            return False, user_data, "Account not found"
        
        account = user_data["accounts"][account_index]
        
        # Check if sufficient balance for debit
        if transaction_type == "debit" and account["balance"] < amount:
            return False, user_data, "Insufficient balance"
        
        # Update balance
        if transaction_type == "credit":
            account["balance"] += amount
        else:
            account["balance"] -= amount
        
        # Create transaction record
        transaction = {
            "transaction_id": str(uuid.uuid4()),
            "type": transaction_type,
            "amount": amount,
            "description": description,
            "timestamp": datetime.now().isoformat(),
            "balance_after": account["balance"]
        }
        
        # Add transaction to account
        if "transactions" not in account:
            account["transactions"] = []
        
        account["transactions"].append(transaction)
        
        return True, user_data, "Transaction added successfully"
    
    return atomic_transaction(user_id, transaction_func)

# Function to add loan
def add_loan(user_id, loan_data):
    """
    Add a loan to user
    Returns (success, message) tuple
    """
    def transaction_func(user_data):
        if "loans" not in user_data:
            user_data["loans"] = []
        
        # Add loan ID if not present
        if "loan_id" not in loan_data:
            loan_data["loan_id"] = str(uuid.uuid4())
        
        # Add timestamp if not present
        if "timestamp" not in loan_data:
            loan_data["timestamp"] = datetime.now().isoformat()
        
        # Add loan to user data
        user_data["loans"].append(loan_data)
        
        # If loan is approved, add transaction to primary account
        if loan_data.get("status") == "approved":
            if "accounts" in user_data and len(user_data["accounts"]) > 0:
                account = user_data["accounts"][0]
                
                # Update balance
                account["balance"] += loan_data.get("amount", 0)
                
                # Create transaction record
                transaction = {
                    "transaction_id": str(uuid.uuid4()),
                    "type": "credit",
                    "amount": loan_data.get("amount", 0),
                    "description": f"Loan disbursement - {loan_data.get('type', 'Loan')}",
                    "timestamp": datetime.now().isoformat(),
                    "balance_after": account["balance"],
                    "reference": loan_data.get("loan_id")
                }
                
                # Add transaction to account
                if "transactions" not in account:
                    account["transactions"] = []
                
                account["transactions"].append(transaction)
        
        return True, user_data, "Loan added successfully"
    
    return atomic_transaction(user_id, transaction_func)

# Function to update loan status
def update_loan_status(user_id, loan_id, status):
    """
    Update loan status
    Returns (success, message) tuple
    """
    def transaction_func(user_data):
        if "loans" not in user_data:
            return False, user_data, "No loans found"
        
        # Find loan by ID
        loan_index = None
        for i, loan in enumerate(user_data["loans"]):
            if loan.get("loan_id") == loan_id:
                loan_index = i
                break
        
        if loan_index is None:
            return False, user_data, "Loan not found"
        
        # Update loan status
        user_data["loans"][loan_index]["status"] = status
        user_data["loans"][loan_index]["updated_at"] = datetime.now().isoformat()
        
        # If loan is approved, add transaction to primary account
        if status == "approved" and user_data["loans"][loan_index].get("status") != "approved":
            if "accounts" in user_data and len(user_data["accounts"]) > 0:
                account = user_data["accounts"][0]
                loan = user_data["loans"][loan_index]
                
                # Update balance
                account["balance"] += loan.get("amount", 0)
                
                # Create transaction record
                transaction = {
                    "transaction_id": str(uuid.uuid4()),
                    "type": "credit",
                    "amount": loan.get("amount", 0),
                    "description": f"Loan disbursement - {loan.get('type', 'Loan')}",
                    "timestamp": datetime.now().isoformat(),
                    "balance_after": account["balance"],
                    "reference": loan_id
                }
                
                # Add transaction to account
                if "transactions" not in account:
                    account["transactions"] = []
                
                account["transactions"].append(transaction)
        
        return True, user_data, "Loan status updated successfully"
    
    return atomic_transaction(user_id, transaction_func)

# Function to transfer funds
def transfer_funds(user_id, from_account_index, to_account_number, amount, description):
    """
    Transfer funds between accounts
    Returns (success, message) tuple
    """
    # First, debit from sender's account
    debit_success, debit_message = add_transaction(
        user_id, 
        from_account_index, 
        "debit", 
        amount, 
        f"Transfer to {to_account_number}: {description}"
    )
    
    if not debit_success:
        return False, debit_message
    
    # Find recipient by account number
    recipient_id = None
    recipient_account_index = None
    
    users = get_all_users()
    for uid, user_data in users.items():
        if "accounts" in user_data:
            for i, account in enumerate(user_data["accounts"]):
                if account.get("account_number") == to_account_number:
                    recipient_id = uid
                    recipient_account_index = i
                    break
            if recipient_id:
                break
    
    if not recipient_id:
        # Rollback the debit transaction
        add_transaction(
            user_id,
            from_account_index,
            "credit",
            amount,
            f"Reversal of failed transfer to {to_account_number}: Recipient not found"
        )
        return False, "Recipient account not found"
    
    # Credit to recipient's account
    credit_success, credit_message = add_transaction(
        recipient_id,
        recipient_account_index,
        "credit",
        amount,
        f"Transfer from {load_user_data(user_id)['accounts'][from_account_index]['account_number']}: {description}"
    )
    
    if not credit_success:
        # Rollback the debit transaction
        add_transaction(
            user_id,
            from_account_index,
            "credit",
            amount,
            f"Reversal of failed transfer to {to_account_number}: {credit_message}"
        )
        return False, f"Error crediting recipient account: {credit_message}"
    
    return True, "Transfer completed successfully"
