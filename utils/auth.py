import os
import json
import re
import uuid
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from utils.security import hash_password, verify_password
from utils.db import load_user_data, save_user_data, get_all_users

# Function to login user
def login_user(email, password):
    """
    Authenticate a user with email and password
    Returns (success, user_id, message)
    """
    # Get all users
    users = get_all_users()
    
    # Find user by email
    user_id = None
    for uid, user_data in users.items():
        if user_data.get("email") == email:
            user_id = uid
            break
    
    if not user_id:
        return False, None, "Invalid email or password"
    
    # Load user data
    user_data = load_user_data(user_id)
    
    # Check if account is locked
    if user_data.get("security", {}).get("login_attempts", 0) >= 5:
        last_attempt = datetime.fromisoformat(user_data.get("security", {}).get("last_attempt", datetime.now().isoformat()))
        if datetime.now() - last_attempt < timedelta(minutes=30):
            return False, None, "Account is locked due to too many failed login attempts. Try again later."
        else:
            # Reset login attempts after 30 minutes
            user_data["security"]["login_attempts"] = 0
            save_user_data(user_data)
    
    # Verify password
    if not verify_password(password, user_data.get("password", "")):
        # Increment login attempts
        if "security" not in user_data:
            user_data["security"] = {}
        
        user_data["security"]["login_attempts"] = user_data.get("security", {}).get("login_attempts", 0) + 1
        user_data["security"]["last_attempt"] = datetime.now().isoformat()
        save_user_data(user_data)
        
        return False, None, "Invalid email or password"
    
    # Reset login attempts on successful login
    if "security" in user_data:
        user_data["security"]["login_attempts"] = 0
        user_data["security"]["last_login"] = datetime.now().isoformat()
        save_user_data(user_data)
    
    return True, user_id, "Login successful"

# Function to register user
def register_user(user_data):
    """
    Register a new user
    Returns (success, message)
    """
    # Validate email format
    if not re.match(r"[^@]+@[^@]+\.[^@]+", user_data.get("email", "")):
        return False, "Invalid email format"
    
    # Check if email already exists
    users = get_all_users()
    for uid, data in users.items():
        if data.get("email") == user_data.get("email"):
            return False, "Email already registered"
    
    # Generate user ID if not provided
    if "user_id" not in user_data:
        user_data["user_id"] = str(uuid.uuid4())
    
    # Set creation timestamp
    user_data["created_at"] = datetime.now().isoformat()
    
    # Save user data
    success, message = save_user_data(user_data)
    
    return success, message

# Function to generate OTP
def generate_otp():
    """Generate a 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=6))

# Function to verify OTP
def verify_otp(otp, secret):
    """Verify OTP against secret"""
    return otp == secret

# Function to send OTP via email
def send_otp_email(email, otp):
    """Send OTP to user's email"""
    # In a real application, you would use SMTP to send emails
    # For this demo, we'll just print the OTP
    print(f"OTP for {email}: {otp}")
    
    # Simulated email sending
    # In a real application, you would use:
    '''
    sender_email = "noreply@nuvanabank.com"
    sender_password = "your_app_password"  # NOTE: Store credentials securely, not hardcoded!
    
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = "Nuvana Bank - Your OTP for Login"
    
    # Correctly formatted multi-line HTML string
    body = f"""
    <html>
    <body>
        <h2>Nuvana Bank - One-Time Password</h2>
        <p>Your OTP for login is: <strong>{otp}</strong></p>
        <p>This OTP is valid for 5 minutes.</p>
        <p>If you did not request this OTP, please ignore this email.</p>
        <p>Regards,<br>Nuvana Bank Team</p>
    </body>
    </html>
    """
    
    message.attach(MIMEText(body, "html"))
    
    try:
        # Ensure you have enabled 'less secure app access' or use app passwords for Gmail
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, message.as_string())
        server.quit()
        print(f"OTP email sent successfully to {email}") # Added success message
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
    '''
    
    return True

# Function to reset password
def reset_password(email):
    """
    Reset user password
    Returns (success, message)
    """
    # Find user by email
    users = get_all_users()
    user_id = None
    
    for uid, user_data in users.items():
        if user_data.get("email") == email:
            user_id = uid
            break
    
    if not user_id:
        return False, "Email not found"
    
    # Generate temporary password
    temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    
    # Update user data
    user_data = load_user_data(user_id)
    user_data["password"] = hash_password(temp_password)
    user_data["security"]["password_reset"] = True
    user_data["security"]["last_password_change"] = datetime.now().isoformat()
    
    # Save user data
    success, message = save_user_data(user_data)
    
    if success:
        # Send email with temporary password
        # In a real application, you would send an email here
        print(f"Temporary password for {email}: {temp_password}")
        return True, "Password reset successful. Check your email for the temporary password."
    else:
        return False, message

# Function to change password
def change_password(user_id, current_password, new_password):
    """
    Change user password
    Returns (success, message)
    """
    # Load user data
    user_data = load_user_data(user_id)
    
    if not user_data:
        return False, "User not found"
    
    # Verify current password
    if not verify_password(current_password, user_data.get("password", "")):
        return False, "Current password is incorrect"
    
    # Update password
    user_data["password"] = hash_password(new_password)
    user_data["security"]["last_password_change"] = datetime.now().isoformat()
    if "password_reset" in user_data["security"]:
        user_data["security"]["password_reset"] = False
    
    # Save user data
    success, message = save_user_data(user_data)
    
    return success, "Password changed successfully" if success else message

# Enable or disable 2FA for a user
def toggle_2fa(user_id, enable):
    """
    Enable or disable 2FA for a user.
    Returns (success, message).
    """
    # Load user data
    user_data = load_user_data(user_id)
    
    if not user_data:
        return False, "User not found"
    
    # Update 2FA setting
    if "security" not in user_data:
        user_data["security"] = {}
    
    user_data["security"]["2fa_enabled"] = enable
    
    # Save user data
    success, message = save_user_data(user_data)
    
    return success, f"2FA {'enabled' if enable else 'disabled'} successfully" if success else message
