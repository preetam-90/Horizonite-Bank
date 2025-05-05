import streamlit as st
import os
import json
import hashlib
import base64
import time
import uuid
from datetime import datetime, timedelta
import pyotp
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string
from streamlit_option_menu import option_menu
from utils.auth import login_user, register_user, verify_otp, generate_otp, send_otp_email
from utils.db import save_user_data, load_user_data, get_all_users, atomic_transaction
from utils.security import hash_password, verify_password, generate_session_id
from pages.dashboard import show_dashboard
from pages.transactions import show_transactions, perform_transfer
from pages.Loans import show_loans, show_emi_calculator
from pages.settings import show_settings
from pages.Admin import show_admin_panel
from pages.Help import show_help
from home import *

# Set page configuration
st.set_page_config(
    page_title="Nuvana Bank",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
css_file = "assets/css/style.css"
try:
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning(f"CSS file {css_file} not found. Some styles may not be applied correctly.")
    # Use basic styles as fallback
    st.markdown("""
    <style>
    .stApp {
        background-color: #f7fafc;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_data' not in st.session_state:
    st.session_state.user_data = None
if 'session_id' not in st.session_state:
    st.session_state.session_id = None
if 'last_activity' not in st.session_state:
    st.session_state.last_activity = None
if 'theme' not in st.session_state:
    st.session_state.theme = "light"
if 'otp_secret' not in st.session_state:
    st.session_state.otp_secret = None
if 'temp_user_data' not in st.session_state:
    st.session_state.temp_user_data = None
if 'notification' not in st.session_state:
    st.session_state.notification = None
if 'notification_type' not in st.session_state:
    st.session_state.notification_type = None

# Create necessary directories
os.makedirs("data/users", exist_ok=True)
os.makedirs("data/sessions", exist_ok=True)
os.makedirs("data/logs", exist_ok=True)

# Function to check session timeout
def check_session_timeout():
    if st.session_state.logged_in and st.session_state.last_activity:
        current_time = datetime.now()
        last_activity = st.session_state.last_activity
        # Session timeout after 30 minutes of inactivity
        if (current_time - last_activity).total_seconds() > 1800:  # 30 minutes
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.user_data = None
            st.session_state.session_id = None
            st.session_state.last_activity = None
            st.warning("Your session has expired. Please log in again.")
            return True
    return False

# Function to update last activity
def update_last_activity():
    if st.session_state.logged_in:
        st.session_state.last_activity = datetime.now()

# Function to show notification
def show_notification():
    if st.session_state.notification:
        if st.session_state.notification_type == "success":
            st.success(st.session_state.notification)
        elif st.session_state.notification_type == "error":
            st.error(st.session_state.notification)
        elif st.session_state.notification_type == "warning":
            st.warning(st.session_state.notification)
        else:
            st.info(st.session_state.notification)
        
        # Clear notification after displaying
        st.session_state.notification = None
        st.session_state.notification_type = None

# Function to set notification
def set_notification(message, type="info"):
    st.session_state.notification = message
    st.session_state.notification_type = type

# Function to log activity
def log_activity(user_id, activity_type, details=None):
    timestamp = datetime.now().isoformat()
    log_entry = {
        "timestamp": timestamp,
        "user_id": user_id,
        "activity_type": activity_type,
        "details": details
    }
    
    log_file = f"data/logs/activity_log_{datetime.now().strftime('%Y%m%d')}.json"
    
    try:
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                logs = json.load(f)
        else:
            logs = []
        
        logs.append(log_entry)
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=4)
    except Exception as e:
        print(f"Error logging activity: {e}")

# Login page
def show_login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        
        # Bank logo
        st.image("assets/images/nuvana_logo.png", width=200)
        st.markdown("<h1 class='bank-title'>Nuvana Bank</h1>", unsafe_allow_html=True)
        st.markdown("<p class='bank-slogan'>Your Trusted Financial Partner</p>", unsafe_allow_html=True)
        
        # Login form
        with st.form("login_form"):
            st.subheader("Login to Your Account")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            
            col1, col2 = st.columns(2)
            with col1:
                remember_me = st.checkbox("Remember me")
            with col2:
                st.markdown("<div style='text-align: right;'><a href='#' onclick='forgot_password()'>Forgot Password?</a></div>", unsafe_allow_html=True)
            
            submit_button = st.form_submit_button("Login")
            
            if submit_button:
                if not email or not password:
                    st.error("Please fill in all fields")
                else:
                    success, user_id, message = login_user(email, password)
                    
                    if success:
                        # If 2FA is enabled, show OTP screen
                        user_data = load_user_data(user_id)
                        if user_data.get("security", {}).get("2fa_enabled", False):
                            st.session_state.temp_user_data = user_data
                            st.session_state.otp_secret = generate_otp()
                            send_otp_email(user_data["email"], st.session_state.otp_secret)
                            set_notification("OTP has been sent to your email", "info")
                            st.rerun()
                        else:
                            # Login successful
                            st.session_state.logged_in = True
                            st.session_state.user_id = user_id
                            st.session_state.user_data = user_data
                            st.session_state.session_id = generate_session_id()
                            st.session_state.last_activity = datetime.now()
                            
                            log_activity(user_id, "login", {"method": "password"})
                            set_notification("Login successful", "success")
                            st.rerun()
                    else:
                        st.error(message)
        
        # Register link
        st.markdown("<div style='text-align: center; margin-top: 20px;'>Don't have an account? <a href='#' onclick='show_register()'>Register here</a></div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# OTP verification page
def show_otp_verification():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        
        # Bank logo
        st.image("assets/images/nuvana_logo.png", width=200)
        st.markdown("<h1 class='bank-title'>Nuvana Bank</h1>", unsafe_allow_html=True)
        
        # OTP form
        with st.form("otp_form"):
            st.subheader("Two-Factor Authentication")
            st.markdown("<p>Please enter the OTP sent to your email</p>", unsafe_allow_html=True)
            
            otp = st.text_input("OTP", max_chars=6)
            
            submit_button = st.form_submit_button("Verify")
            
            if submit_button:
                if not otp:
                    st.error("Please enter the OTP")
                else:
                    if verify_otp(otp, st.session_state.otp_secret):
                        # OTP verification successful
                        user_data = st.session_state.temp_user_data
                        user_id = user_data["user_id"]
                        
                        st.session_state.logged_in = True
                        st.session_state.user_id = user_id
                        st.session_state.user_data = user_data
                        st.session_state.session_id = generate_session_id()
                        st.session_state.last_activity = datetime.now()
                        st.session_state.temp_user_data = None
                        st.session_state.otp_secret = None
                        
                        log_activity(user_id, "login", {"method": "2fa"})
                        set_notification("Login successful", "success")
                        st.rerun()
                    else:
                        st.error("Invalid OTP. Please try again.")
        
        # Resend OTP button
        if st.button("Resend OTP"):
            st.session_state.otp_secret = generate_otp()
            send_otp_email(st.session_state.temp_user_data["email"], st.session_state.otp_secret)
            st.info("OTP has been resent to your email")
        
        # Cancel button
        if st.button("Cancel"):
            st.session_state.temp_user_data = None
            st.session_state.otp_secret = None
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

# Registration page
def show_registration_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        
        # Bank logo
        st.image("assets/images/nuvana_logo.png", width=200)
        st.markdown("<h1 class='bank-title'>Nuvana Bank</h1>", unsafe_allow_html=True)
        st.markdown("<p class='bank-slogan'>Your Trusted Financial Partner</p>", unsafe_allow_html=True)
        
        # Registration form
        with st.form("registration_form"):
            st.subheader("Open a New Account")
            
            # Personal Information
            st.markdown("<h3>Personal Information</h3>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                full_name = st.text_input("Full Name")
                email = st.text_input("Email")
                phone = st.text_input("Phone Number")
            
            with col2:
                dob = st.date_input("Date of Birth")
                pan = st.text_input("PAN Number")
                aadhar = st.text_input("Aadhar Number")
            
            address = st.text_area("Address")
            
            # Account Information
            st.markdown("<h3>Account Information</h3>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                account_type = st.selectbox("Account Type", ["Savings", "Current", "Salary"])
                initial_deposit = st.number_input("Initial Deposit (₹)", min_value=1000.0, step=1000.0)
            
            with col2:
                password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
            
            # Terms and Conditions
            terms = st.checkbox("I agree to the terms and conditions")
            
            submit_button = st.form_submit_button("Register")
            
            if submit_button:
                # Validate inputs
                if not all([full_name, email, phone, address, pan, aadhar, password, confirm_password]):
                    st.error("Please fill in all required fields")
                elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    st.error("Please enter a valid email address")
                elif not re.match(r"^[0-9]{10}$", phone):
                    st.error("Please enter a valid 10-digit phone number")
                elif not re.match(r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$", pan):
                    st.error("Please enter a valid PAN number (e.g., ABCDE1234F)")
                elif not re.match(r"^[0-9]{12}$", aadhar):
                    st.error("Please enter a valid 12-digit Aadhar number")
                elif password != confirm_password:
                    st.error("Passwords do not match")
                elif len(password) < 8:
                    st.error("Password must be at least 8 characters long")
                elif not terms:
                    st.error("Please agree to the terms and conditions")
                else:
                    # Create user data
                    user_data = {
                        "user_id": str(uuid.uuid4()),
                        "full_name": full_name,
                        "email": email,
                        "phone": phone,
                        "dob": dob.isoformat(),
                        "pan": pan,
                        "aadhar": aadhar,
                        "address": address,
                        "password": hash_password(password),
                        "created_at": datetime.now().isoformat(),
                        "accounts": [
                            {
                                "account_number": f"NB{random.randint(10000000, 99999999)}",
                                "account_type": account_type,
                                "balance": initial_deposit,
                                "created_at": datetime.now().isoformat(),
                                "status": "Active",
                                "transactions": [
                                    {
                                        "transaction_id": str(uuid.uuid4()),
                                        "type": "credit",
                                        "amount": initial_deposit,
                                        "description": "Initial deposit",
                                        "timestamp": datetime.now().isoformat(),
                                        "balance_after": initial_deposit
                                    }
                                ]
                            }
                        ],
                        "loans": [],
                        "security": {
                            "2fa_enabled": False,
                            "last_password_change": datetime.now().isoformat(),
                            "login_attempts": 0
                        },
                        "preferences": {
                            "theme": "light",
                            "notifications": {
                                "email": True,
                                "sms": True
                            }
                        },
                        "role": "user"  # Default role
                    }
                    
                    # Save user data
                    success, message = save_user_data(user_data)
                    
                    if success:
                        log_activity(user_data["user_id"], "registration", {"email": email})
                        set_notification("Registration successful! You can now log in.", "success")
                        st.rerun()
                    else:
                        st.error(message)
        
        # Login link
        st.markdown("<div style='text-align: center; margin-top: 20px;'>Already have an account? <a href='#' onclick='show_login()'>Login here</a></div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# Main application
def main():
    # Check session timeout
    if check_session_timeout():
        return
    
    # Update last activity
    update_last_activity()
    
    # Show notification if any
    show_notification()
    
    # Handle authentication
    if not st.session_state.logged_in:
        if st.session_state.temp_user_data and st.session_state.otp_secret:
            show_otp_verification()
        elif st.query_params.get("page") == "register":
            show_registration_page()
        else:
            show_login_page()
        return
    
    # Load user data
    user_data = load_user_data(st.session_state.user_id)
    if not user_data:
        st.session_state.logged_in = False
        st.error("User data not found. Please log in again.")
        return
    
    st.session_state.user_data = user_data
    
    # Sidebar navigation
    with st.sidebar:
        st.image("assets/images/nuvana_logo.png", width=100)
        st.markdown(f"<h3>Welcome, {user_data['full_name'].split()[0]}</h3>", unsafe_allow_html=True)
        
        # Display account number and balance
        primary_account = user_data["accounts"][0]
        st.markdown(f"<p>Account: {primary_account['account_number']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='balance'>Balance: ₹{primary_account['balance']:,.2f}</p>", unsafe_allow_html=True)
        
        # Navigation menu
        selected = option_menu(
            "home",
            ["admin", "dashboard", "help", "loans", "settings", "transactions"],
            icons=["person", "speedometer", "question", "currency-exchange", "gear", "cash-stack"],
            menu_icon="cast",
            default_index=0,
            orientation="vertical"
        )
        
        # Admin panel for admin users
        if user_data.get("role") == "admin":
            if st.button("Admin Panel", key="admin_panel"):
                selected = "Admin Panel"
        
        # Theme toggle
        theme = st.selectbox("Theme", ["Light", "Dark"], index=0 if st.session_state.theme == "light" else 1)
        if theme == "Light" and st.session_state.theme != "light":
            st.session_state.theme = "light"
            st.rerun()
        elif theme == "Dark" and st.session_state.theme != "dark":
            st.session_state.theme = "dark"
            st.rerun()
        
        # Logout button
        if st.button("Logout"):
            log_activity(st.session_state.user_id, "logout")
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.user_data = None
            st.session_state.session_id = None
            st.session_state.last_activity = None
            set_notification("Logged out successfully", "success")
            st.rerun()
    
    # Main content
    if selected == "Dashboard":
        show_dashboard(st.session_state.user_data)
    elif selected == "Transactions":
        show_transactions(user_data)
    elif selected == "Loans":
        show_loans(user_data)
    elif selected == "EMI Calculator":
        show_emi_calculator()
    elif selected == "Settings":
        show_settings(user_data)
    elif selected == "Help":
        # Remove the help section from the sidebar
        show_help()
    elif selected == "Admin Panel" and user_data.get("role") == "admin":
        show_admin_panel()

if __name__ == "__main__":
    main()