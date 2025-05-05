import streamlit as st
import json
import os
import hashlib
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import random
import time

# Set page configuration
st.set_page_config(
    page_title="Horizonite Bank",
    page_icon="🏦",
    layout="centered",  # Change from "wide" to "centered"
    initial_sidebar_state="expanded"
)

# Custom CSS for elegant UI
st.markdown("""
<style>
    body {
        background-color: #1a1c23;
        color: #e4e6eb;
    }
    .main .block-container {
        background-color: #1a1c23;
        padding: 1rem;
    }
    .main-header {
        font-size: 2.5rem;
        color: #3dbfff;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #3dbfff;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #2d303e;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 1rem;
        transition: transform 0.2s ease;
    }
    .card:hover {
        transform: translateY(-3px);
    }
    .success-msg {
        padding: 0.75rem;
        border-radius: 0.25rem;
        background-color: rgba(76, 175, 80, 0.15);
        color: #4CAF50;
        margin-bottom: 1rem;
    }
    .error-msg {
        padding: 0.75rem;
        border-radius: 0.25rem;
        background-color: rgba(229, 57, 53, 0.15);
        color: #e53935;
        margin-bottom: 1rem;
    }
    .info-msg {
        padding: 0.75rem;
        border-radius: 0.25rem;
        background-color: rgba(61, 191, 255, 0.15);
        color: #3dbfff;
        margin-bottom: 1rem;
    }
    .btn-primary {
        background-color: #3dbfff;
        color: #1a1c23;
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        border: none;
        cursor: pointer;
        transition: background-color 0.2s ease;
    }
    .btn-primary:hover {
        background-color: #61cdff;
    }
    .btn-secondary {
        background-color: #3e4251;
        color: #e4e6eb;
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        border: none;
        cursor: pointer;
        transition: background-color 0.2s ease;
    }
    .btn-secondary:hover {
        background-color: #4c506b;
    }
    .sidebar .sidebar-content {
        background-color: #252836;
        color: #e4e6eb;
    }
    /* Make sidebar buttons match dark theme */
    .sidebar .stButton button {
        background-color: #3e4251;
        color: #e4e6eb;
        border: none;
        width: 100%;
        text-align: left;
        margin-bottom: 0.5rem;
        border-radius: 0.25rem;
        padding: 0.5rem 1rem;
        transition: background-color 0.2s ease;
    }
    .sidebar .stButton button:hover {
        background-color: #4c506b;
    }
    .account-balance {
        font-size: 2rem;
        font-weight: 700;
        color: #3dbfff;
    }
    .transaction {
        padding: 0.75rem;
        border-bottom: 1px solid #3e4251;
    }
    .transaction-amount-credit {
        color: #4CAF50;
        font-weight: 600;
    }
    .transaction-amount-debit {
        color: #e53935;
        font-weight: 600;
    }
    /* Form styling */
    input, select, textarea {
        background-color: #2d303e !important;
        border: 1px solid #3e4251 !important;
        border-radius: 0.375rem !important;
        color: #e4e6eb !important;
    }
    input:focus, select:focus, textarea:focus {
        border-color: #3dbfff !important;
        box-shadow: 0 0 0 3px rgba(61, 191, 255, 0.1) !important;
    }
    /* Button styling */
    button[kind="primary"] {
        background-color: #3dbfff !important;
        border-color: #3dbfff !important;
    }
    button[kind="primary"]:hover {
        background-color: #61cdff !important;
        border-color: #61cdff !important;
    }
    /* Checkbox and Radio styling */
    .stCheckbox > label > div[role="checkbox"],
    .stRadio > label > div[role="radio"] {
        background-color: #2d303e !important;
        border-color: #3e4251 !important;
    }
    /* Slider styling */
    .stSlider > div > div > div {
        background-color: #3dbfff !important;
    }
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1a1c23 !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #b8bac0 !important;
    }
    .stTabs [aria-selected="true"] {
        color: #3dbfff !important;
        border-bottom-color: #3dbfff !important;
    }
    /* Override Streamlit elements */
    .stTextInput > label, .stNumberInput > label, .stSelectbox > label, .stTextArea > label {
        color: #b8bac0 !important;
    }
    .css-1adrfps {
        background-color: #2d303e !important;
    }
    /* Login and registration page styling */
    .login-container {
        background-color: #2d303e !important;
    }
    .login-divider {
        border-top: 1px solid #3e4251;
        position: relative;
        margin: 1.5rem 0;
        text-align: center;
    }
    .login-divider-text {
        position: relative;
        top: -0.7rem;
        background-color: #2d303e;
        padding: 0 0.5rem;
    }
    a {
        color: #3dbfff !important;
        text-decoration: none !important;
    }
    a:hover {
        text-decoration: underline !important;
    }
    /* Fix header and other elements */
    h1, h2, h3, h4, h5, h6 {
        color: #e4e6eb !important;
    }
    p {
        color: #b8bac0 !important;
    }
    .stMarkdown {
        color: #b8bac0 !important;
    }
    .profile-container {
        padding: 1.5rem;
        background-color: #1a1c23;
    }
    .profile-header {
        background: linear-gradient(90deg, #1E3A8A 0%, #2c4ec9 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        position: relative;
        overflow: hidden;
    }
    .profile-header h1 {
        font-size: 1.8rem;
        margin-bottom: 0.5rem;
        color: white !important;
    }
    .profile-header p {
        opacity: 0.9;
        color: #e4e6eb !important;
    }
    .profile-avatar {
        width: 80px;
        height: 80px;
        background-color: #3dbfff;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 2rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .info-card {
        background-color: #2d303e;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
        margin-bottom: 2rem;
        transition: transform 0.2s;
        position: relative;
        overflow: hidden;
    }
    .info-card:hover {
        transform: translateY(-5px);
    }
    .info-card h3 {
        font-size: 1.2rem;
        margin-bottom: 1.5rem;
        color: #e4e6eb !important;
        border-bottom: 1px solid #3e4251;
        padding-bottom: 0.5rem;
    }
    .info-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 5px;
        height: 100%;
        background-color: #3dbfff;
    }
    .account-card::before {
        background-color: #4CAF50;
    }
    .info-item {
        display: flex;
        justify-content: space-between;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #3e4251;
    }
    .info-item:last-child {
        border-bottom: none;
    }
    .info-label {
        color: #a0a3ad;
        font-weight: 400;
    }
    .info-value {
        color: #e4e6eb;
        font-weight: 500;
    }
    .highlight-value {
        color: #3dbfff;
        font-weight: 600;
        font-size: 1.2rem;
    }
    .edit-form-container {
        background-color: #2d303e;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
    }
    .edit-form-header {
        font-size: 1.2rem;
        margin-bottom: 1.5rem;
        color: #e4e6eb !important;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .section-icon {
        display: inline-flex;
        width: 30px;
        height: 30px;
        background-color: rgba(61, 191, 255, 0.15);
        color: #3dbfff;
        border-radius: 50%;
        align-items: center;
        justify-content: center;
        margin-right: 8px;
    }
    .update-button {
        width: 100%;
        padding: 0.75rem;
        background-color: #3dbfff;
        color: #1a1c23;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        margin-top: 1rem;
        transition: background-color 0.2s;
    }
    .update-button:hover {
        background-color: #61cdff;
    }
    .clickable-card {
        cursor: pointer;
        transition: transform 0.3s, box-shadow 0.3s;
    }
    .clickable-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
    }
    .auth-btn {
        background: linear-gradient(135deg, #3182CE 0%, #2C5282 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 20px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        margin-bottom: 8px;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
    }
    .auth-btn:hover {
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        transform: translateY(-2px);
    }
    .auth-btn.secondary {
        background: #2e3346;
        border: 1px solid #3e4251;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'current_page' not in st.session_state:
    st.session_state.current_page = "login"
if 'notification' not in st.session_state:
    st.session_state.notification = None
if 'notification_type' not in st.session_state:
    st.session_state.notification_type = None

# File paths
DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
ACCOUNTS_FILE = os.path.join(DATA_DIR, "accounts.json")
TRANSACTIONS_FILE = os.path.join(DATA_DIR, "transactions.json")

# Create data directory if it doesn't exist
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Initialize data files if they don't exist
def initialize_data_files():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            json.dump({}, f)
    
    if not os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, 'w') as f:
            json.dump({}, f)
    
    if not os.path.exists(TRANSACTIONS_FILE):
        with open(TRANSACTIONS_FILE, 'w') as f:
            json.dump({}, f)

initialize_data_files()

# Helper functions
def hash_password(password):
    """Hash a password for storing."""
    return hashlib.sha256(password.encode()).hexdigest()

def load_data(file_path):
    """Load data from a JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_data(data, file_path):
    """Save data to a JSON file."""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def register_user(username, password, email, full_name, address, phone):
    """Register a new user."""
    users = load_data(USERS_FILE)
    
    if username in users:
        return False, "Username already exists"
    
    users[username] = {
        "password": hash_password(password),
        "email": email,
        "full_name": full_name,
        "address": address,
        "phone": phone,
        "created_at": datetime.datetime.now().isoformat()
    }
    
    save_data(users, USERS_FILE)
    
    # Create an account for the user
    accounts = load_data(ACCOUNTS_FILE)
    account_number = f"NB{random.randint(10000000, 99999999)}"
    
    accounts[username] = {
        "account_number": account_number,
        "balance": 0,
        "account_type": "Savings",
        "status": "Active",
        "created_at": datetime.datetime.now().isoformat()
    }
    
    save_data(accounts, ACCOUNTS_FILE)
    
    return True, "Registration successful"

def authenticate_user(username, password):
    """Authenticate a user."""
    users = load_data(USERS_FILE)
    
    if username not in users:
        return False, "Invalid username or password"
    
    if users[username]["password"] != hash_password(password):
        return False, "Invalid username or password"
    
    return True, "Login successful"

def get_account_details(username):
    """Get account details for a user."""
    accounts = load_data(ACCOUNTS_FILE)
    
    if username not in accounts:
        return None
    
    return accounts[username]

def get_user_details(username):
    """Get user details."""
    users = load_data(USERS_FILE)
    
    if username not in users:
        return None
    
    user_data = users[username].copy()
    user_data.pop("password", None)  # Remove password for security
    
    return user_data

def get_transactions(username):
    """Get transactions for a user."""
    transactions = load_data(TRANSACTIONS_FILE)
    
    if username not in transactions:
        return []
    
    return transactions[username]

def add_transaction(username, transaction_type, amount, description):
    """Add a transaction for a user."""
    transactions = load_data(TRANSACTIONS_FILE)
    
    if username not in transactions:
        transactions[username] = []
    
    transaction = {
        "id": len(transactions[username]) + 1,
        "type": transaction_type,
        "amount": amount,
        "description": description,
        "timestamp": datetime.datetime.now().isoformat()
    }
    
    transactions[username].append(transaction)
    save_data(transactions, TRANSACTIONS_FILE)
    
    # Update account balance
    accounts = load_data(ACCOUNTS_FILE)
    
    if transaction_type == "credit":
        accounts[username]["balance"] += amount
    else:
        accounts[username]["balance"] -= amount
    
    save_data(accounts, ACCOUNTS_FILE)

def calculate_emi(principal, rate, time):
    """Calculate EMI."""
    rate = rate / (12 * 100)  # Monthly interest rate
    time = time * 12  # Total number of months
    
    emi = (principal * rate * (1 + rate) ** time) / ((1 + rate) ** time - 1)
    
    return emi

# Navigation functions
def navigate_to(page):
    st.session_state.current_page = page

def show_notification(message, type="info"):
    st.session_state.notification = message
    st.session_state.notification_type = type

# UI Components
def display_header():
    # Removed the duplicate title
    pass

def display_notification():
    if st.session_state.notification:
        if st.session_state.notification_type == "success":
            st.markdown(f'<div class="success-msg">{st.session_state.notification}</div>', unsafe_allow_html=True)
        elif st.session_state.notification_type == "error":
            st.markdown(f'<div class="error-msg">{st.session_state.notification}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="info-msg">{st.session_state.notification}</div>', unsafe_allow_html=True)
        
        # Clear notification after displaying
        st.session_state.notification = None
        st.session_state.notification_type = None

def display_sidebar():
    with st.sidebar:
        # Improved Bank header with subtle gradient and shadow
        st.markdown('''
        <div style="
            background: linear-gradient(135deg, #2B3990 0%, #3949AB 100%);
            padding: 25px 15px;
            border-radius: 12px;
            margin-bottom: 20px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);">
            <h2 style="color: white; font-weight: 700; margin-bottom: 6px; font-size: 24px;">Horizonite Bank</h2>
            <p style="color: rgba(255, 255, 255, 0.85); font-size: 13px; margin: 0;">Your Trusted Financial Partner</p>
        </div>
        ''', unsafe_allow_html=True)
        
        if st.session_state.logged_in:
            # Enhanced profile section with better styling
            first_letter = st.session_state.username[0].upper() if st.session_state.username else "Q"
            st.markdown(f'''
            <div style="
                background-color: #252836;
                padding: 16px;
                border-radius: 12px;
                margin-bottom: 20px;
                display: flex;
                align-items: center;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);">
                <div style="
                    width: 42px;
                    height: 42px;
                    background: linear-gradient(135deg, #3182CE 0%, #2C5282 100%);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 19px;
                    font-weight: 600;
                    margin-right: 14px;
                    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);">
                    {first_letter}
                </div>
                <div>
                    <p style="margin: 0; font-size: 13px; color: #8A94A6; margin-bottom: 2px;">Welcome,</p>
                    <p style="margin: 0; color: #ffffff; font-weight: 500; font-size: 15px;">{st.session_state.username}</p>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
            # Enhanced navigation styling with active state indicator
            current_page = st.session_state.current_page
            
            st.markdown('''
            <style>
            .sidebar .stButton button {
                background-color: #1e2130;
                border: 1px solid #2e3346;
                border-radius: 10px;
                padding: 12px 15px;
                margin-bottom: 10px;
                color: #ffffff;
                display: flex;
                align-items: center;
                font-size: 14px;
                font-weight: normal;
                width: 100%;
                transition: all 0.2s ease;
                position: relative;
                overflow: hidden;
                text-align: left;
            }
            .sidebar .stButton button:hover {
                background-color: #2a2e3d;
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            .sidebar .stButton button:active {
                transform: translateY(0px);
            }
            .nav-icon {
                display: inline-block;
                margin-right: 10px;
                width: 20px;
                text-align: center;
            }
            .active-nav-item {
                background: linear-gradient(135deg, #2c3251 0%, #262c41 100%) !important;
                border-left: 3px solid #3182CE !important;
            }
            
            /* Always show button outline */
            .sidebar .stButton button[kind="secondary"] {
                border-left: 3px solid #2e3346 !important;
            }
            .sidebar .stButton button[kind="secondary"]:hover {
                border-left: 3px solid #3182CE !important;
            }
            </style>
            ''', unsafe_allow_html=True)
            
            # Navigation section title
            st.markdown('<p style="color: #8A94A6; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; font-weight: 600;">MAIN NAVIGATION</p>', unsafe_allow_html=True)
            
            # Dashboard button with active state
            dashboard_class = "active-nav-item" if current_page == "dashboard" else ""
            st.markdown(f'''
            <button id="dashboard-btn" class="{dashboard_class}" style="display: none;"></button>
            ''', unsafe_allow_html=True)
            if st.button("🏠 Dashboard", key="dashboard_btn", use_container_width=True):
                navigate_to("dashboard")
            
            # Account Details button with active state
            account_class = "active-nav-item" if current_page == "account_details" else ""
            st.markdown(f'''
            <button id="account-btn" class="{account_class}" style="display: none;"></button>
            ''', unsafe_allow_html=True)
            if st.button("👤 Account Details", key="account_btn", use_container_width=True):
                navigate_to("account_details")
            
            # Transactions button with active state
            transactions_class = "active-nav-item" if current_page == "transactions" else ""
            st.markdown(f'''
            <button id="transactions-btn" class="{transactions_class}" style="display: none;"></button>
            ''', unsafe_allow_html=True)
            if st.button("📊 Transactions", key="transactions_btn", use_container_width=True):
                navigate_to("transactions")
            
            # Apply active state for buttons via JavaScript
            st.markdown('''
            <script>
            document.addEventListener('DOMContentLoaded', function() {
                // Set timeout to ensure Streamlit elements are fully loaded
                setTimeout(function() {
                    // Apply style to all navigation buttons first
                    const allNavButtons = document.querySelectorAll('.sidebar .stButton button');
                    allNavButtons.forEach(function(btn) {
                        btn.style.borderLeft = '3px solid #2e3346';
                    });
                    
                    // Get hidden buttons with active states
                    const dashboardBtn = document.getElementById('dashboard-btn');
                    const accountBtn = document.getElementById('account-btn');
                    const transactionsBtn = document.getElementById('transactions-btn');
                    const transferBtn = document.getElementById('transfer-btn');
                    const emiBtn = document.getElementById('emi-btn');
                    
                    // Apply active class to actual buttons
                    if (dashboardBtn && dashboardBtn.classList.contains('active-nav-item')) {
                        const btn = document.querySelector('[key="dashboard_btn"]');
                        if (btn) {
                            btn.style.borderLeft = '3px solid #3182CE';
                            btn.style.background = 'linear-gradient(135deg, #2c3251 0%, #262c41 100%)';
                        }
                    }
                    
                    if (accountBtn && accountBtn.classList.contains('active-nav-item')) {
                        const btn = document.querySelector('[key="account_btn"]');
                        if (btn) {
                            btn.style.borderLeft = '3px solid #3182CE';
                            btn.style.background = 'linear-gradient(135deg, #2c3251 0%, #262c41 100%)';
                        }
                    }
                    
                    if (transactionsBtn && transactionsBtn.classList.contains('active-nav-item')) {
                        const btn = document.querySelector('[key="transactions_btn"]');
                        if (btn) {
                            btn.style.borderLeft = '3px solid #3182CE';
                            btn.style.background = 'linear-gradient(135deg, #2c3251 0%, #262c41 100%)';
                        }
                    }
                    
                    if (transferBtn && transferBtn.classList.contains('active-nav-item')) {
                        const btn = document.querySelector('[key="sidebar_transfer_btn"]');
                        if (btn) {
                            btn.style.borderLeft = '3px solid #3182CE';
                            btn.style.background = 'linear-gradient(135deg, #2c3251 0%, #262c41 100%)';
                        }
                    }
                    
                    if (emiBtn && emiBtn.classList.contains('active-nav-item')) {
                        const btn = document.querySelector('[key="sidebar_emi_btn"]');
                        if (btn) {
                            btn.style.borderLeft = '3px solid #3182CE';
                            btn.style.background = 'linear-gradient(135deg, #2c3251 0%, #262c41 100%)';
                        }
                    }
                }, 500); // 500ms delay to ensure elements are loaded
            });
            </script>
            ''', unsafe_allow_html=True)
            
            # Money Management section
            st.markdown('<p style="color: #8A94A6; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; margin-top: 25px; margin-bottom: 12px; font-weight: 600;">MONEY MANAGEMENT</p>', unsafe_allow_html=True)
            
            # Transfer Money button with active state
            transfer_class = "active-nav-item" if current_page == "transfer" else ""
            st.markdown(f'''<button id="transfer-btn" class="{transfer_class}" style="display: none;"></button>''', unsafe_allow_html=True)
            if st.button("💸 Transfer Money", key="sidebar_transfer_btn", use_container_width=True):
                navigate_to("transfer")
            
            # EMI Calculator button with active state
            emi_class = "active-nav-item" if current_page == "emi_calculator" else ""
            st.markdown(f'''<button id="emi-btn" class="{emi_class}" style="display: none;"></button>''', unsafe_allow_html=True)
            if st.button("📝 EMI Calculator", key="sidebar_emi_btn", use_container_width=True):
                navigate_to("emi_calculator")
            
            # Add logout at bottom with spacing
            st.markdown('<div style="margin-top: 40px;"></div>', unsafe_allow_html=True)
            if st.button("🚪 Logout", key="logout_btn", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.username = ""
                navigate_to("login")
                
        else:
            # Login and Register buttons
            st.markdown('''
            <style>
            .auth-btn {
                background: linear-gradient(135deg, #3182CE 0%, #2C5282 100%);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 20px;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.3s ease;
                width: 100%;
                margin-bottom: 8px;
                text-align: center;
                box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
            }
            .auth-btn:hover {
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
                transform: translateY(-2px);
            }
            .auth-btn.secondary {
                background: #2e3346;
                border: 1px solid #3e4251;
            }
            </style>
            ''', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Login", key="login_btn", use_container_width=True):
                    navigate_to("login")
            
            with col2:
                if st.button("Register", key="register_btn", use_container_width=True):
                    navigate_to("register")
                    
            # Apply styles to buttons via JavaScript
            st.markdown('''
            <script>
                document.addEventListener('DOMContentLoaded', function() {
                    const loginBtn = document.querySelector('[key="login_btn"]');
                    const registerBtn = document.querySelector('[key="register_btn"]');
                    
                    if (loginBtn) loginBtn.classList.add('auth-btn');
                    if (registerBtn) registerBtn.classList.add('auth-btn', 'secondary');
                });
            </script>
            ''', unsafe_allow_html=True)

def account_details_page():
    st.markdown("""
    <style>
        .profile-container {
            padding: 1.5rem;
            background-color: #1a1c23;
        }
        .profile-header {
            background: linear-gradient(90deg, #1E3A8A 0%, #2c4ec9 100%);
            padding: 2rem;
            border-radius: 12px;
            color: white;
            margin-bottom: 2rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            position: relative;
            overflow: hidden;
        }
        .profile-header h1 {
            font-size: 1.8rem;
            margin-bottom: 0.5rem;
            color: white !important;
        }
        .profile-header p {
            opacity: 0.9;
            color: #e4e6eb !important;
        }
        .profile-avatar {
            width: 80px;
            height: 80px;
            background-color: #3dbfff;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 2rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        .info-card {
            background-color: #2d303e;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
            margin-bottom: 2rem;
            transition: transform 0.2s;
            position: relative;
            overflow: hidden;
        }
        .info-card:hover {
            transform: translateY(-5px);
        }
        .info-card h3 {
            font-size: 1.2rem;
            margin-bottom: 1.5rem;
            color: #e4e6eb !important;
            border-bottom: 1px solid #3e4251;
            padding-bottom: 0.5rem;
        }
        .info-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 5px;
            height: 100%;
            background-color: #3dbfff;
        }
        .account-card::before {
            background-color: #4CAF50;
        }
        .info-item {
            display: flex;
            justify-content: space-between;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid #3e4251;
        }
        .info-item:last-child {
            border-bottom: none;
        }
        .info-label {
            color: #a0a3ad;
            font-weight: 400;
        }
        .info-value {
            color: #e4e6eb;
            font-weight: 500;
        }
        .highlight-value {
            color: #3dbfff;
            font-weight: 600;
            font-size: 1.2rem;
        }
        .edit-form-container {
            background-color: #2d303e;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
        }
        .edit-form-header {
            font-size: 1.2rem;
            margin-bottom: 1.5rem;
            color: #e4e6eb !important;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .section-icon {
            display: inline-flex;
            width: 30px;
            height: 30px;
            background-color: rgba(61, 191, 255, 0.15);
            color: #3dbfff;
            border-radius: 50%;
            align-items: center;
            justify-content: center;
            margin-right: 8px;
        }
        .update-button {
            width: 100%;
            padding: 0.75rem;
            background-color: #3dbfff;
            color: #1a1c23;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            margin-top: 1rem;
            transition: background-color 0.2s;
        }
        .update-button:hover {
            background-color: #61cdff;
        }
    </style>
    """, unsafe_allow_html=True)
    
    account = get_account_details(st.session_state.username)
    user = get_user_details(st.session_state.username)
    
    if not account or not user:
        show_notification("Account not found", "error")
        navigate_to("login")
        return
    
    # Format opening date
    try:
        opening_date = datetime.datetime.fromisoformat(account["created_at"]).strftime("%d %b %Y")
    except:
        opening_date = account["created_at"]
    
    # Get user's first letter for the avatar
    first_letter = user["full_name"][0].upper() if user["full_name"] else "U"
    
    # Profile container
    st.markdown('<div class="profile-container">', unsafe_allow_html=True)
    
    # Profile header with avatar
    st.markdown(f'''
    <div class="profile-header">
        <div class="profile-avatar">{first_letter}</div>
        <h1>{user["full_name"]}</h1>
        <p>Account holder since {opening_date}</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Info cards in two columns
    col1, col2 = st.columns(2)
    
    with col1:
        # Personal Information Card
        st.markdown(f'''
        <div class="info-card">
            <h3>
                <span class="section-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                        <circle cx="12" cy="7" r="4"></circle>
                    </svg>
                </span>
                Personal Information
            </h3>
            <div class="info-item">
                <span class="info-label">Full Name</span>
                <span class="info-value">{user["full_name"]}</span>
            </div>
            <div class="info-item">
                <span class="info-label">Email Address</span>
                <span class="info-value">{user["email"]}</span>
            </div>
            <div class="info-item">
                <span class="info-label">Phone Number</span>
                <span class="info-value">{user["phone"]}</span>
            </div>
            <div class="info-item">
                <span class="info-label">Address</span>
                <span class="info-value">{user["address"]}</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        # Account Information Card
        st.markdown(f'''
        <div class="info-card account-card">
            <h3>
                <span class="section-icon" style="background-color: rgba(76, 175, 80, 0.15); color: #4CAF50;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="2" y="5" width="20" height="14" rx="2"></rect>
                        <line x1="2" y1="10" x2="22" y2="10"></line>
                    </svg>
                </span>
                Account Information
            </h3>
            <div class="info-item">
                <span class="info-label">Account Number</span>
                <span class="info-value">{account["account_number"]}</span>
            </div>
            <div class="info-item">
                <span class="info-label">Account Type</span>
                <span class="info-value">{account["account_type"]}</span>
            </div>
            <div class="info-item">
                <span class="info-label">Status</span>
                <span class="info-value" style="color: #4CAF50;">{account["status"]}</span>
            </div>
            <div class="info-item">
                <span class="info-label">Current Balance</span>
                <span class="highlight-value">₹{account["balance"]:,.2f}</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Edit Profile Form
    st.markdown(f'''
    <h3 class="edit-form-header">
        <span class="section-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
            </svg>
        </span>
        Update Your Profile
    </h3>
    ''', unsafe_allow_html=True)
    
    # Edit form in a styled container
    st.markdown('<div class="edit-form-container">', unsafe_allow_html=True)
    
    with st.form("edit_profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            email = st.text_input("Email Address", value=user["email"])
            phone = st.text_input("Phone Number", value=user["phone"])
        
        with col2:
            address = st.text_area("Residential Address", value=user["address"])
        
        submit_button = st.form_submit_button(label="Update Profile", help="Save your profile changes")
        
        if submit_button:
            # Update user details
            users = load_data(USERS_FILE)
            users[st.session_state.username]["email"] = email
            users[st.session_state.username]["phone"] = phone
            users[st.session_state.username]["address"] = address
            
            save_data(users, USERS_FILE)
            
            show_notification("Profile updated successfully", "success")
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close edit form container
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close profile container

def transactions_page():
    st.markdown('<h2 class="sub-header">Transaction History</h2>', unsafe_allow_html=True)
    
    transactions = get_transactions(st.session_state.username)
    
    if not transactions:
        st.info("No transactions found")
        return
    
    # Filter options
    col1, col2 = st.columns(2)
    
    with col1:
        transaction_type = st.selectbox("Filter by Type", ["All", "Credit", "Debit"])
    
    with col2:
        sort_by = st.selectbox("Sort by", ["Newest First", "Oldest First", "Amount (High to Low)", "Amount (Low to High)"])
    
    # Apply filters
    filtered_transactions = transactions.copy()
    
    if transaction_type != "All":
        filtered_transactions = [t for t in filtered_transactions if t["type"].lower() == transaction_type.lower()]
    
    # Apply sorting
    if sort_by == "Newest First":
        filtered_transactions = sorted(filtered_transactions, key=lambda x: x["timestamp"], reverse=True)
    elif sort_by == "Oldest First":
        filtered_transactions = sorted(filtered_transactions, key=lambda x: x["timestamp"])
    elif sort_by == "Amount (High to Low)":
        filtered_transactions = sorted(filtered_transactions, key=lambda x: x["amount"], reverse=True)
    elif sort_by == "Amount (Low to High)":
        filtered_transactions = sorted(filtered_transactions, key=lambda x: x["amount"])
    
    # Display transactions
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    for transaction in filtered_transactions:
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown(f'<div class="transaction">', unsafe_allow_html=True)
            st.markdown(f'<p>{transaction["description"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="font-size: 0.8rem; color: #6b7280;">{transaction["timestamp"]}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'<div class="transaction">', unsafe_allow_html=True)
            if transaction["type"] == "credit":
                st.markdown(f'<p class="transaction-amount-credit">+₹{transaction["amount"]:,.2f}</p>', unsafe_allow_html=True)
            else:
                st.markdown(f'<p class="transaction-amount-debit">-₹{transaction["amount"]:,.2f}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'<div class="transaction">', unsafe_allow_html=True)
            st.markdown(f'<p>{transaction["type"].capitalize()}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Transaction Summary
    st.markdown('<h3>Transaction Summary</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Calculate total credits and debits
        total_credits = sum(t["amount"] for t in transactions if t["type"] == "credit")
        total_debits = sum(t["amount"] for t in transactions if t["type"] == "debit")
        
        # Create a pie chart
        fig, ax = plt.subplots()
        ax.pie([total_credits, total_debits], labels=["Credits", "Debits"], autopct='%1.1f%%', colors=["#047857", "#b91c1c"])
        ax.set_title("Credits vs Debits")
        st.pyplot(fig)
    
    with col2:
        # Create a bar chart of recent transactions
        recent_transactions = sorted(transactions, key=lambda x: x["timestamp"], reverse=True)[:5]
        
        amounts = []
        labels = []
        colors = []
        
        for t in recent_transactions:
            if t["type"] == "credit":
                amounts.append(t["amount"])
                colors.append("#047857")
            else:
                amounts.append(-t["amount"])
                colors.append("#b91c1c")
            
            # Truncate description if too long
            desc = t["description"]
            if len(desc) > 15:
                desc = desc[:12] + "..."
            
            labels.append(desc)
        
        fig, ax = plt.subplots()
        ax.bar(labels, amounts, color=colors)
        ax.set_title("Recent Transactions")
        ax.set_xticklabels(labels, rotation=45, ha="right")
        st.pyplot(fig)

def transfer_page():
    st.markdown('<h2 class="sub-header">Transfer Money</h2>', unsafe_allow_html=True)
    
    account = get_account_details(st.session_state.username)
    
    if not account:
        show_notification("Account not found", "error")
        navigate_to("login")
        return
    
    st.markdown(f'<p>Current Balance: <span class="account-balance">₹{account["balance"]:,.2f}</span></p>', unsafe_allow_html=True)
    
    with st.form("transfer_form"):
        recipient_account = st.text_input("Recipient Account Number")
        amount = st.number_input("Amount", min_value=1.0, step=100.0)
        description = st.text_input("Description")
        
        submit_button = st.form_submit_button("Transfer")
        
        if submit_button:
            if not recipient_account or amount <= 0:
                show_notification("Please fill in all fields with valid values", "error")
            elif amount > account["balance"]:
                show_notification("Insufficient balance", "error")
            else:
                # Add debit transaction for sender
                add_transaction(st.session_state.username, "debit", amount, f"Transfer to {recipient_account}: {description}")
                
                # For demo purposes, we'll just show a success message
                # In a real app, you would verify the recipient account and add a credit transaction for them
                show_notification(f"Successfully transferred ₹{amount:,.2f} to {recipient_account}", "success")
                
                # Refresh the page to show updated balance
                st.rerun()
    
    # Quick Transfer
    st.markdown('<h3>Quick Add Money (Demo)</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Add ₹1,000"):
            add_transaction(st.session_state.username, "credit", 1000, "Quick Add")
            show_notification("Added ₹1,000 to your account", "success")
            st.rerun()
    
    with col2:
        if st.button("Add ₹5,000"):
            add_transaction(st.session_state.username, "credit", 5000, "Quick Add")
            show_notification("Added ₹5,000 to your account", "success")
            st.rerun()
    
    with col3:
        if st.button("Add ₹10,000"):
            add_transaction(st.session_state.username, "credit", 10000, "Quick Add")
            show_notification("Added ₹10,000 to your account", "success")
            st.rerun()

def emi_calculator_page():
    # Add custom CSS to make this page wider
    st.markdown('''
    <style>
        /* Make the calculator page wider */
        .main .block-container {
            max-width: 1200px;
            padding-left: 1rem;
            padding-right: 1rem;
            width: 100%;
        }
    </style>
    ''', unsafe_allow_html=True)
    
    st.markdown('''
    <h2 class="sub-header">EMI Calculator</h2>
    <p style="margin-bottom: 20px; color: #8A94A6;">Calculate and visualize your loan EMI with detailed breakdown</p>
    ''', unsafe_allow_html=True)
    
    # Custom CSS for the EMI calculator
    st.markdown('''
    <style>
        .emi-card {
            background: linear-gradient(145deg, #1e2130 0%, #252836 100%);
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 25px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            border: 1px solid #2e3346;
        }
        .emi-result {
            background: linear-gradient(145deg, #2B3990 0%, #3949AB 100%);
            border-radius: 12px;
            padding: 25px;
            color: white;
            text-align: center;
            margin-top: 25px;
            margin-bottom: 25px;
        }
        .emi-amount {
            font-size: 26px;
            font-weight: 700;
            margin-bottom: 10px;
        }
        .emi-details {
            display: flex;
            justify-content: space-between;
            margin-top: 15px;
        }
        .emi-detail-item {
            text-align: center;
            flex: 1;
            padding: 10px;
            border-radius: 8px;
            background-color: rgba(255, 255, 255, 0.1);
            margin: 0 5px;
        }
        .emi-detail-value {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 5px;
        }
        .emi-detail-label {
            font-size: 12px;
            opacity: 0.8;
        }
        .tab-container {
            margin-top: 20px;
        }
        .amortization-table {
            margin-top: 20px;
            width: 100%;
            border-collapse: collapse;
        }
        .amortization-table th, .amortization-table td {
            padding: 10px;
            text-align: right;
            border-bottom: 1px solid #2e3346;
        }
        .amortization-table th {
            background-color: #1e2130;
            color: #8A94A6;
            font-weight: 600;
        }
        .amortization-table tr:hover {
            background-color: #252836;
        }
        .comparison-card {
            background-color: #1e2130;
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 15px;
            border: 1px solid #2e3346;
        }
        .comparison-title {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 10px;
            color: #fff;
        }
        .comparison-value {
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 5px;
            color: #3182CE;
        }
    </style>
    ''', unsafe_allow_html=True)
    
    # Top row layout
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown('<div class="emi-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="margin-bottom: 20px; font-size: 20px;">Loan Details</h3>', unsafe_allow_html=True)
        
        # Use number input with formatting for more precise control
        st.markdown('<p style="margin-bottom: 5px; color: #8A94A6; font-size: 14px;">Loan Amount (₹)</p>', unsafe_allow_html=True)
        loan_amount = st.slider("", 10000, 10000000, 1000000, step=10000, format="%d", key="loan_amount_slider", label_visibility="collapsed")
        
        # Custom number input for more precise amount
        col_a, col_b = st.columns([3, 1])
        with col_a:
            loan_amount_precise = st.number_input("Enter exact amount (optional)", min_value=10000, max_value=10000000, value=loan_amount, step=1000, label_visibility="collapsed")
            if loan_amount_precise != loan_amount:
                loan_amount = loan_amount_precise
        
        st.markdown('<p style="margin-bottom: 5px; margin-top: 15px; color: #8A94A6; font-size: 14px;">Interest Rate (%)</p>', unsafe_allow_html=True)
        interest_rate = st.slider("", 1.0, 20.0, 8.5, step=0.1, format="%.1f", key="interest_rate_slider", label_visibility="collapsed")
        
        st.markdown('<p style="margin-bottom: 5px; margin-top: 15px; color: #8A94A6; font-size: 14px;">Loan Term</p>', unsafe_allow_html=True)
        
        # Use radio buttons for term type selection
        term_type = st.radio("Term Type", ["Years", "Months"], horizontal=True)
        
        if term_type == "Years":
            loan_term_years = st.slider("", 1, 30, 20, step=1, key="loan_term_slider", label_visibility="collapsed")
            loan_term = loan_term_years  # Years
        else:
            loan_term_months = st.slider("", 1, 360, 240, step=1, key="loan_term_slider_months", label_visibility="collapsed")
            loan_term = loan_term_months / 12  # Convert months to years
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Calculate EMI immediately without button
        emi = calculate_emi(loan_amount, interest_rate, loan_term)
        total_payment = emi * loan_term * 12
        total_interest = total_payment - loan_amount
        
        # Display EMI result in a styled card
        st.markdown('<div class="emi-result">', unsafe_allow_html=True)
        st.markdown(f'<p style="margin-bottom: 10px; font-size: 14px; opacity: 0.9;">Your Monthly Payment</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="emi-amount">₹{emi:,.2f}</div>', unsafe_allow_html=True)
        
        # Display key metrics in a row
        st.markdown('<div class="emi-details">', unsafe_allow_html=True)
        
        # Principal amount
        st.markdown(f'''
        <div class="emi-detail-item">
            <div class="emi-detail-value">₹{loan_amount:,.0f}</div>
            <div class="emi-detail-label">Principal</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Total interest
        st.markdown(f'''
        <div class="emi-detail-item">
            <div class="emi-detail-value">₹{total_interest:,.0f}</div>
            <div class="emi-detail-label">Interest</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Total payment
        st.markdown(f'''
        <div class="emi-detail-item">
            <div class="emi-detail-value">₹{total_payment:,.0f}</div>
            <div class="emi-detail-label">Total Payment</div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Loan comparison section
        st.markdown('<div class="emi-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="margin-bottom: 20px; font-size: 20px;">Loan Comparison</h3>', unsafe_allow_html=True)
        
        # Create comparison options
        comparison_options = st.radio(
            "Compare with:",
            ["Lower Interest Rate", "Higher Interest Rate", "Shorter Term", "Longer Term"],
            horizontal=True
        )
        
        # Calculate comparison EMI based on selection
        if comparison_options == "Lower Interest Rate":
            compare_interest = max(interest_rate - 2, 1.0)
            compare_term = loan_term
            comparison_title = f"Interest Rate: {compare_interest}% (2% lower)"
        elif comparison_options == "Higher Interest Rate":
            compare_interest = min(interest_rate + 2, 20.0)
            compare_term = loan_term
            comparison_title = f"Interest Rate: {compare_interest}% (2% higher)"
        elif comparison_options == "Shorter Term":
            compare_interest = interest_rate
            compare_term = max(loan_term - 5, 1) if term_type == "Years" else max(loan_term - 0.5, 0.1)
            years_text = f"{compare_term:.1f} years" if compare_term != int(compare_term) else f"{int(compare_term)} years"
            comparison_title = f"Term: {years_text} (shorter)"
        else:  # Longer Term
            compare_interest = interest_rate
            compare_term = min(loan_term + 5, 30) if term_type == "Years" else min(loan_term + 0.5, 30)
            years_text = f"{compare_term:.1f} years" if compare_term != int(compare_term) else f"{int(compare_term)} years"
            comparison_title = f"Term: {years_text} (longer)"
        
        # Calculate comparison EMI
        compare_emi = calculate_emi(loan_amount, compare_interest, compare_term)
        compare_total = compare_emi * compare_term * 12
        compare_interest_total = compare_total - loan_amount
        
        # Display EMI difference
        emi_diff = emi - compare_emi
        monthly_savings = f"+₹{abs(emi_diff):,.2f}" if emi_diff < 0 else f"-₹{abs(emi_diff):,.2f}"
        total_diff = total_payment - compare_total
        total_savings = f"+₹{abs(total_diff):,.2f}" if total_diff < 0 else f"-₹{abs(total_diff):,.2f}"
        
        # Display comparison cards
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            st.markdown(f'''
            <div class="comparison-card">
                <div style="font-size: 14px; color: #8A94A6;">Monthly Payment</div>
                <div class="comparison-value">₹{compare_emi:,.2f}</div>
                <div style="font-size: 14px; color: {'#4ADE80' if emi_diff > 0 else '#F87171'};">
                    {monthly_savings} per month
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col_c2:
            st.markdown(f'''
            <div class="comparison-card">
                <div style="font-size: 14px; color: #8A94A6;">Total Payment</div>
                <div class="comparison-value">₹{compare_total:,.0f}</div>
                <div style="font-size: 14px; color: {'#4ADE80' if total_diff > 0 else '#F87171'};">
                    {total_savings} overall
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="emi-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="margin-bottom: 20px; font-size: 20px;">Loan Visualization</h3>', unsafe_allow_html=True)
        
        # Create tabs for different visualizations
        tab1, tab2 = st.tabs(["Payment Breakdown", "Payment Schedule"])
        
        with tab1:
            # Create a pie chart for EMI breakdown with improved styling
            fig = plt.figure(figsize=(12, 7))
            ax = fig.add_subplot(111)
            
            # Custom colors
            colors = ['#3182CE', '#9F7AEA']
            
            # Create data
            labels = ["Principal", "Interest"]
            sizes = [loan_amount, total_interest]
            
            # Create pie chart with custom styling
            wedges, texts, autotexts = ax.pie(
                sizes, 
                labels=labels, 
                autopct='%1.1f%%', 
                startangle=90, 
                colors=colors,
                wedgeprops={'width': 0.4, 'edgecolor': 'white', 'linewidth': 1},
                textprops={'fontsize': 12, 'color': 'white'}
            )
            
            # Style pie chart
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                
            ax.set_title("Loan Breakdown", color='white', fontsize=16, pad=20)
            
            # Set background color
            fig.patch.set_facecolor('#252836')
            ax.set_facecolor('#252836')
            
            # Equal aspect ratio for circular pie
            ax.axis('equal')
            
            # Add total values
            plt.annotate(
                f"Principal: ₹{loan_amount:,.0f}\nInterest: ₹{total_interest:,.0f}\nTotal: ₹{total_payment:,.0f}",
                xy=(0, -0.1),
                xycoords='axes fraction',
                ha='center',
                va='center',
                color='white',
                fontsize=12
            )
            
            st.pyplot(fig)
        
        with tab2:
            # Create a line chart for payment schedule
            fig, ax = plt.subplots(figsize=(12, 7))
            
            # Create data for the payment schedule
            years = list(range(1, int(loan_term) + 2)) if loan_term > 1 else [0.25, 0.5, 0.75, 1, 1.25]
            remaining_principal = [loan_amount]
            
            # Calculate remaining principal over time
            principal_remaining = loan_amount
            for _ in range(1, len(years)):
                for __ in range(12):  # 12 months in a year
                    interest_for_month = principal_remaining * (interest_rate / (12 * 100))
                    principal_for_month = emi - interest_for_month
                    principal_remaining = max(0, principal_remaining - principal_for_month)
                remaining_principal.append(principal_remaining)
            
            # Plot the line chart with improved styling
            ax.plot(years, remaining_principal, marker='o', markersize=6, linewidth=3, color='#3182CE')
            
            # Add monthly payment annotation
            ax.annotate(
                f"Monthly Payment: ₹{emi:,.2f}",
                xy=(years[len(years)//2], remaining_principal[len(years)//2]),
                xytext=(0, 30),
                textcoords='offset points',
                color='white',
                fontsize=12,
                bbox=dict(boxstyle="round,pad=0.3", facecolor='#3949AB', alpha=0.8),
                arrowprops=dict(arrowstyle='->', color='white')
            )
            
            # Style the chart
            ax.set_xlabel("Years", color='white', fontsize=12)
            ax.set_ylabel("Remaining Principal (₹)", color='white', fontsize=12)
            ax.set_title("Principal Remaining Over Time", color='white', fontsize=16, pad=20)
            
            # Format y-axis labels
            ax.get_yaxis().set_major_formatter(
                plt.FuncFormatter(lambda x, loc: f"₹{int(x):,}")
            )
            
            # Style grid
            ax.grid(True, linestyle='--', alpha=0.3)
            
            # Style ticks
            ax.tick_params(colors='white', which='both')
            
            # Set background color
            fig.patch.set_facecolor('#252836')
            ax.set_facecolor('#252836')
            
            # Style spines
            for spine in ax.spines.values():
                spine.set_edgecolor('#3f4663')
            
            st.pyplot(fig)
        
        st.markdown('</div>', unsafe_allow_html=True)

def login_page():
    # Create a container for the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-container" style="background-color: #f0f4f8; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);">', unsafe_allow_html=True)
        
        # Bank header - simplified to remove any black bar
        st.markdown('<h1 style="color: #1E3A8A; text-align: center; margin-bottom: 0.5rem;">Horizonite Bank</h1>', unsafe_allow_html=True)
        st.markdown('<p style="color: #4b5563; text-align: center; margin-bottom: 1.5rem;">Your Trusted Financial Partner</p>', unsafe_allow_html=True)
        
        # Login form
        with st.form("login_form", clear_on_submit=False):
            st.markdown('<div class="login-form">', unsafe_allow_html=True)
            
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            # Remember me checkbox and forgot password link
            col1, col2 = st.columns(2)
            with col1:
                remember_me = st.checkbox("Remember me")
            with col2:
                st.markdown('<div style="text-align: right; padding-top: 5px;"><a href="#" style="color: #1E3A8A; text-decoration: none;">Forgot password?</a></div>', unsafe_allow_html=True)
            
            # Login button
            submit_button = st.form_submit_button("Login", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            if submit_button:
                if not username or not password:
                    show_notification("Please fill in all fields", "error")
                else:
                    success, message = authenticate_user(username, password)
                    
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        navigate_to("dashboard")
                        show_notification(message, "success")
                    else:
                        show_notification(message, "error")
        
        # Divider
        st.markdown('<div class="login-divider"><span class="login-divider-text" style="background-color: #f0f4f8; color: #6b7280;">OR</span></div>', unsafe_allow_html=True)
        
        # Register link
        st.markdown('<div class="login-footer" style="color: #4b5563;">Don\'t have an account? <a href="#" id="register-link" style="color: #1E3A8A; text-decoration: none;">Register here</a></div>', unsafe_allow_html=True)
        
        # Add a button below for better UX
        if st.button("Create New Account", key="create_account_btn"):
            navigate_to("register")
            
        st.markdown('</div>', unsafe_allow_html=True)

def register_page():
    # Create a container for the registration form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-container" style="background-color: #f0f4f8; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);">', unsafe_allow_html=True)
        
        # Bank header - simplified to match login page
        st.markdown('<h1 style="color: #1E3A8A; text-align: center; margin-bottom: 0.5rem;">Create Account</h1>', unsafe_allow_html=True)
        st.markdown('<p style="color: #4b5563; text-align: center; margin-bottom: 1.5rem;">Join Horizonite Bank today</p>', unsafe_allow_html=True)
        
        # Registration form
        with st.form("register_form", clear_on_submit=False):
            st.markdown('<div class="login-form">', unsafe_allow_html=True)
            
            # Personal details
            st.markdown('<h3 style="font-size: 1.2rem; margin-bottom: 1rem; color: #4b5563;">Personal Information</h3>', unsafe_allow_html=True)
            
            full_name = st.text_input("Full Name", placeholder="Enter your full name")
            
            col1, col2 = st.columns(2)
            with col1:
                email = st.text_input("Email", placeholder="Enter your email")
            with col2:
                phone = st.text_input("Phone Number", placeholder="Enter your phone number")
            
            # Account details
            st.markdown('<h3 style="font-size: 1.2rem; margin-top: 1.5rem; margin-bottom: 1rem; color: #4b5563;">Account Information</h3>', unsafe_allow_html=True)
            
            username = st.text_input("Username", placeholder="Choose a username")
            
            col1, col2 = st.columns(2)
            with col1:
                password = st.text_input("Password", type="password", placeholder="Create password")
            with col2:
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm password")
            
            address = st.text_area("Address", placeholder="Enter your full address")
            
            # Terms and conditions
            terms = st.checkbox("I agree to the terms and conditions")
            
            # Submit button
            submit_button = st.form_submit_button("Create Account", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            if submit_button:
                if not all([full_name, email, phone, username, password, confirm_password, address]):
                    show_notification("Please fill in all fields", "error")
                elif password != confirm_password:
                    show_notification("Passwords do not match", "error")
                elif not terms:
                    show_notification("Please agree to the terms and conditions", "error")
                else:
                    success, message = register_user(username, password, email, full_name, address, phone)
                    
                    if success:
                        navigate_to("login")
                        show_notification(message, "success")
                    else:
                        show_notification(message, "error")
        
        # Divider
        st.markdown('<div class="login-divider"><span class="login-divider-text" style="background-color: #f0f4f8; color: #6b7280;">OR</span></div>', unsafe_allow_html=True)
        
        # Login link
        st.markdown('<div class="login-footer" style="color: #4b5563;">Already have an account? <a href="#" id="login-link" style="color: #1E3A8A; text-decoration: none;">Login here</a></div>', unsafe_allow_html=True)
        
        # Add a button below for better UX
        if st.button("Back to Login", key="back_to_login_btn"):
            navigate_to("login")
            
        st.markdown('</div>', unsafe_allow_html=True)

def dashboard_page():
    # Custom CSS for dashboard with dark theme
    st.markdown("""
    <style>
        body {
            background-color: #1a1c23;
            color: #e4e6eb;
        }
        .main .block-container {
            background-color: #1a1c23;
            padding: 1rem;
        }
        .dashboard-container {
            padding: 1.5rem;
            background-color: #1a1c23;
        }
        .welcome-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 2rem;
            background: linear-gradient(90deg, #1E3A8A 0%, #2c4ec9 100%);
            padding: 1.5rem 2rem;
            border-radius: 12px;
            color: white;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        }
        .welcome-text h1 {
            font-size: 1.8rem;
            font-weight: 700;
            margin: 0;
            color: white;
        }
        .welcome-text p {
            font-size: 1rem;
            margin: 0.5rem 0 0 0;
            opacity: 0.9;
        }
        .date-time {
            font-size: 0.9rem;
            opacity: 0.8;
        }
        .balance-card {
            background-color: #2d303e;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
            height: 100%;
            border-left: 5px solid #4CAF50;
            transition: transform 0.2s;
        }
        .balance-card:hover {
            transform: translateY(-5px);
        }
        .balance-card h2 {
            font-size: 1.2rem;
            color: #b8bac0;
            margin-bottom: 1rem;
            font-weight: 600;
        }
        .balance-amount {
            font-size: 2.5rem;
            font-weight: 700;
            color: #3dbfff;
            margin-bottom: 0.5rem;
        }
        .account-card {
            background-color: #2d303e;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
            height: 100%;
            border-left: 5px solid #3dbfff;
            transition: transform 0.2s;
        }
        .account-card:hover {
            transform: translateY(-5px);
        }
        .account-card h2 {
            font-size: 1.2rem;
            color: #b8bac0;
            margin-bottom: 1rem;
            font-weight: 600;
        }
        .account-detail {
            margin-bottom: 0.5rem;
            display: flex;
            justify-content: space-between;
        }
        .account-label {
            color: #a0a3ad;
        }
        .account-value {
            font-weight: 500;
            color: #e4e6eb;
        }
        .action-cards {
            display: flex;
            gap: 1rem;
            margin-bottom: 2rem;
        }
        .action-card {
            background-color: #2d303e;
            border-radius: 12px;
            padding: 1.5rem;
            flex: 1;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
            transition: transform 0.3s;
            cursor: pointer;
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-bottom: 1rem;
            border-top: 3px solid #2d303e;
        }
        .action-card:hover {
            transform: translateY(-5px);
            border-top-color: #3dbfff;
        }
        .action-icon {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 1rem;
        }
        .action-icon.transfer {
            background-color: rgba(61, 191, 255, 0.15);
            color: #3dbfff;
        }
        .action-icon.calculator {
            background-color: rgba(255, 196, 0, 0.15);
            color: #ffc400;
        }
        .action-icon.transactions {
            background-color: rgba(76, 175, 80, 0.15);
            color: #4CAF50;
        }
        .action-title {
            font-weight: 600;
            font-size: 1.1rem;
            margin-bottom: 0.5rem;
            color: #e4e6eb;
        }
        .action-description {
            font-size: 0.9rem;
            color: #a0a3ad;
            margin-bottom: 1rem;
        }
        .action-btn {
            background-color: #3e4251;
            color: #b8bac0;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            font-size: 0.9rem;
            font-weight: 500;
            text-decoration: none;
            transition: background-color 0.3s;
        }
        .action-btn:hover {
            background-color: #4c506b;
        }
        .transactions-card {
            background-color: #2d303e;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
            margin-top: 2rem;
        }
        .transactions-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
        }
        .transactions-title {
            font-size: 1.2rem;
            font-weight: 600;
            color: #b8bac0;
        }
        .view-all {
            font-size: 0.9rem;
            color: #3dbfff;
            text-decoration: none;
            font-weight: 500;
        }
        .transaction-item {
            display: flex;
            align-items: center;
            padding: 1rem 0;
            border-bottom: 1px solid #3e4251;
        }
        .transaction-icon {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 1rem;
            flex-shrink: 0;
        }
        .transaction-icon.credit {
            background-color: rgba(76, 175, 80, 0.15);
            color: #4CAF50;
        }
        .transaction-icon.debit {
            background-color: rgba(229, 57, 53, 0.15);
            color: #e53935;
        }
        .transaction-details {
            flex: 1;
        }
        .transaction-title {
            font-weight: 500;
            margin-bottom: 0.25rem;
            color: #e4e6eb;
        }
        .transaction-date {
            font-size: 0.8rem;
            color: #a0a3ad;
        }
        .transaction-amount {
            font-weight: 600;
        }
        .transaction-amount.credit {
            color: #4CAF50;
        }
        .transaction-amount.debit {
            color: #e53935;
        }
        .quick-stats {
            display: flex;
            gap: 1rem;
            margin-bottom: 2rem;
        }
        .stat-card {
            background-color: #2d303e;
            border-radius: 12px;
            padding: 1.5rem;
            flex: 1;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
            transition: transform 0.2s;
            border-bottom: 3px solid #3dbfff;
        }
        .stat-card:hover {
            transform: translateY(-5px);
        }
        .stat-label {
            font-size: 0.9rem;
            color: #a0a3ad;
            margin-bottom: 0.5rem;
        }
        .stat-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: #3dbfff;
        }
        .stat-trend {
            font-size: 0.8rem;
            margin-top: 0.5rem;
            color: #a0a3ad;
        }
        .trend-up {
            color: #4CAF50;
        }
        .trend-down {
            color: #e53935;
        }
        /* Override Streamlit elements for dark mode */
        .stButton button {
            background-color: #3e4251;
            color: #e4e6eb;
            border: none;
        }
        .stButton button:hover {
            background-color: #4c506b;
            color: #ffffff;
        }
        .element-container, div.row-widget.stButton, div.row-widget.stDownloadButton {
            background-color: transparent !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    account = get_account_details(st.session_state.username)
    user = get_user_details(st.session_state.username)
    
    if not account:
        show_notification("Account not found", "error")
        navigate_to("login")
        return
    
    # Dashboard container
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    
    # Welcome header with date and time
    st.markdown(f'''
    <div class="welcome-header">
        <div class="welcome-text">
            <h1>Welcome back, {user["full_name"].split()[0]}!</h1>
            <p>Your financial dashboard is ready</p>
        </div>
        <div class="date-time">
            {datetime.datetime.now().strftime("%A, %d %B %Y")}
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Account overview and balance section
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f'''
        <div class="account-card">
            <h2>Account Overview</h2>
            <div class="account-detail">
                <span class="account-label">Account Number</span>
                <span class="account-value">{account["account_number"]}</span>
            </div>
            <div class="account-detail">
                <span class="account-label">Account Type</span>
                <span class="account-value">{account["account_type"]}</span>
            </div>
            <div class="account-detail">
                <span class="account-label">Status</span>
                <span class="account-value">{account["status"]}</span>
            </div>
            <div class="account-detail">
                <span class="account-label">Created</span>
                <span class="account-value">{datetime.datetime.fromisoformat(account["created_at"]).strftime("%d %b %Y")}</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="balance-card">
            <h2>Current Balance</h2>
            <div class="balance-amount">₹{account["balance"]:,.2f}</div>
            <p style="color: #a0a3ad;">Available to spend</p>
        </div>
        ''', unsafe_allow_html=True)
    
    # Quick stats
    st.markdown('<div class="quick-stats">', unsafe_allow_html=True)
    
    # Get transaction data for stats
    transactions = get_transactions(st.session_state.username)
    
    # Calculate monthly income (credits in the current month)
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year
    
    monthly_income = sum([
        tx["amount"] for tx in transactions 
        if tx["type"] == "credit" 
        and datetime.datetime.fromisoformat(tx["timestamp"]).month == current_month
        and datetime.datetime.fromisoformat(tx["timestamp"]).year == current_year
    ])
    
    # Calculate monthly expenses (debits in the current month)
    monthly_expenses = sum([
        tx["amount"] for tx in transactions 
        if tx["type"] == "debit" 
        and datetime.datetime.fromisoformat(tx["timestamp"]).month == current_month
        and datetime.datetime.fromisoformat(tx["timestamp"]).year == current_year
    ])
    
    # Calculate previous month stats for trends
    prev_month = current_month - 1 if current_month > 1 else 12
    prev_year = current_year if current_month > 1 else current_year - 1
    
    prev_income = sum([
        tx["amount"] for tx in transactions 
        if tx["type"] == "credit" 
        and datetime.datetime.fromisoformat(tx["timestamp"]).month == prev_month
        and datetime.datetime.fromisoformat(tx["timestamp"]).year == prev_year
    ])
    
    prev_expenses = sum([
        tx["amount"] for tx in transactions 
        if tx["type"] == "debit" 
        and datetime.datetime.fromisoformat(tx["timestamp"]).month == prev_month
        and datetime.datetime.fromisoformat(tx["timestamp"]).year == prev_year
    ])
    
    # Calculate trend percentages
    income_trend = ((monthly_income - prev_income) / max(prev_income, 1)) * 100 if prev_income > 0 else 100
    expense_trend = ((monthly_expenses - prev_expenses) / max(prev_expenses, 1)) * 100 if prev_expenses > 0 else 100
    
    # Stat 1: Monthly Income
    st.markdown(f'''
    <div class="stat-card">
        <div class="stat-label">Monthly Income</div>
        <div class="stat-value">₹{monthly_income:,.2f}</div>
        <div class="stat-trend {'trend-up' if income_trend >= 0 else 'trend-down'}">
            {'+' if income_trend >= 0 else ''}{income_trend:.1f}% from last month
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Stat 2: Monthly Expenses
    st.markdown(f'''
    <div class="stat-card">
        <div class="stat-label">Monthly Expenses</div>
        <div class="stat-value">₹{monthly_expenses:,.2f}</div>
        <div class="stat-trend {'trend-down' if expense_trend <= 0 else 'trend-up'}">
            {'+' if expense_trend >= 0 else ''}{expense_trend:.1f}% from last month
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Stat 3: Savings Rate
    savings_rate = ((monthly_income - monthly_expenses) / monthly_income * 100) if monthly_income > 0 else 0
    st.markdown(f'''
    <div class="stat-card">
        <div class="stat-label">Savings Rate</div>
        <div class="stat-value">{savings_rate:.1f}%</div>
        <div class="stat-trend">Monthly savings</div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown('<h3 style="margin-bottom: 1.5rem; font-size: 1.4rem; color: #e4e6eb; font-weight: 600;">Quick Actions</h3>', unsafe_allow_html=True)

    # Action cards - using a more modern, cleaner design
    col1, col2, col3 = st.columns(3)

    with col1:
        # Transfer Money Card
        st.markdown('''
        <div class="action-card hoverable">
            <div class="action-icon-container">
                <div class="action-icon transfer">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
                    </svg>
                </div>
            </div>
            <div class="action-content">
                <div class="action-title">Transfer Money</div>
                <div class="action-description">Send money to another account</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Simple button with minimal styling
        if st.button("Transfer Money", key="dashboard_transfer_btn"):
            navigate_to("transfer")

    with col2:
        # EMI Calculator Card
        st.markdown('''
        <div class="action-card hoverable">
            <div class="action-icon-container">
                <div class="action-icon calculator">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="4" y="2" width="16" height="20" rx="2"></rect>
                        <line x1="8" y1="6" x2="16" y2="6"></line>
                        <line x1="8" y1="10" x2="16" y2="10"></line>
                        <line x1="8" y1="14" x2="16" y2="14"></line>
                        <line x1="8" y1="18" x2="12" y2="18"></line>
                    </svg>
                </div>
            </div>
            <div class="action-content">
                <div class="action-title">EMI Calculator</div>
                <div class="action-description">Calculate your loan EMI</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Simple button with minimal styling
        if st.button("EMI Calculator", key="dashboard_emi_btn"):
            navigate_to("emi_calculator")

    with col3:
        # View Transactions Card
        st.markdown('''
        <div class="action-card hoverable">
            <div class="action-icon-container">
                <div class="action-icon transactions">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M22 3H2l8 9.46V19l4 2v-8.54L22 3z"></path>
                    </svg>
                </div>
            </div>
            <div class="action-content">
                <div class="action-title">View Transactions</div>
                <div class="action-description">Check your recent transactions</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Simple button with minimal styling
        if st.button("View Transactions", key="dashboard_transactions_btn"):
            navigate_to("transactions")
        
    # Add CSS to style the new cards and hide the buttons but keep them functional
    st.markdown("""
    <style>
    /* Quick action cards styling */
    .action-card {
        background: rgba(40, 45, 55, 0.8);
        border-radius: 16px;
        padding: 20px;
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        border: 1px solid rgba(50, 55, 75, 0.5);
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    }

    .hoverable:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        border-color: rgba(77, 171, 247, 0.5);
    }

    .action-icon-container {
        margin-right: 15px;
    }

    .action-icon {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .action-icon.transfer {
        background: rgba(0, 150, 255, 0.15);
        color: #0096ff;
    }

    .action-icon.calculator {
        background: rgba(255, 184, 0, 0.15);
        color: #FFB800;
    }

    .action-icon.transactions {
        background: rgba(0, 214, 143, 0.15);
        color: #00d68f;
    }

    .action-content {
        flex: 1;
    }

    .action-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 4px;
    }

    .action-description {
        font-size: 0.85rem;
        color: #a0a3ad;
    }

    /* Hide the button text but keep the button functional */
    .stButton button {
        color: transparent;
        background-color: transparent !important;
        border-color: transparent !important;
        width: 100%;
        height: 30px;
        padding: 0;
        margin-top: -20px;
        position: relative;
        z-index: 10;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Recent Transactions
    transactions = get_transactions(st.session_state.username)
    
    st.markdown('''
    <div class="transactions-card">
        <div class="transactions-header">
            <span class="transactions-title">Recent Transactions</span>
            <span class="view-all">View All</span>
        </div>
    ''', unsafe_allow_html=True)
    
    if not transactions:
        st.markdown('<p style="text-align: center; padding: 2rem; color: #a0a3ad;">No transactions found</p>', unsafe_allow_html=True)
    else:
        # Display only the 5 most recent transactions
        recent_transactions = sorted(transactions, key=lambda x: x["timestamp"], reverse=True)[:5]
        
        for transaction in recent_transactions:
            # Format transaction date
            tx_date = datetime.datetime.fromisoformat(transaction["timestamp"]).strftime("%d %b, %Y • %I:%M %p")
            
            # Define SVG icons for credit and debit transactions
            credit_icon = '''<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="19" x2="12" y2="5"></line><polyline points="5 12 12 5 19 12"></polyline></svg>'''
            debit_icon = '''<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><polyline points="19 12 12 19 5 12"></polyline></svg>'''
            
            # Choose the appropriate icon
            icon = credit_icon if transaction["type"] == "credit" else debit_icon
            
            # Create HTML for the transaction item
            transaction_html = f'''
            <div class="transaction-item">
                <div class="transaction-icon {transaction["type"]}">
                    {icon}
                </div>
                <div class="transaction-details">
                    <div class="transaction-title">{transaction["description"]}</div>
                    <div class="transaction-date">{tx_date}</div>
                </div>
                <div class="transaction-amount {transaction["type"]}">
                    {'+' if transaction["type"] == "credit" else '-'}₹{transaction["amount"]:,.2f}
                </div>
            </div>
            '''
            
            # Render the transaction HTML
            st.markdown(transaction_html, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Add View All Transactions button
    if st.button("View All Transactions", key="view_all_transactions"):
        navigate_to("transactions")
    
    # Close the dashboard container
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Matplotlib styling for dark theme
    plt.style.use('dark_background')

def home_page():
    # Use Streamlit's native components for the header section instead of HTML
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.title("Welcome to Horizonite Bank")
        st.markdown("Your trusted partner for secure, innovative, and customer-focused banking solutions.")
        
        # Custom CSS for buttons
        st.markdown("""
        <style>
        /* Style Streamlit buttons */
        .stButton button {
            border-radius: 50px !important;
            font-weight: 600 !important;
            padding: 10px 15px !important;
            font-size: 16px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1) !important;
            margin-top: 20px !important;
            cursor: pointer !important;
            position: relative !important;
            z-index: 10 !important; /* Ensure button is above any potential overlays */
        }
        .stButton button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2) !important;
        }
        .stButton button:active {
            transform: translateY(1px) !important; /* Add feedback on press */
        }
        /* Primary button (Create Account) */
        [data-testid="stHorizontalBlock"] [data-testid="column"]:first-child .stButton button {
            background: linear-gradient(135deg, #4F46E5 0%, #2563EB 100%) !important;
            border: none !important;
            color: white !important;
        }
        /* Secondary button (Login) */
        [data-testid="stHorizontalBlock"] [data-testid="column"]:last-child .stButton button {
            background: rgba(255, 255, 255, 0.1) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            color: white !important;
        }
        /* Ensure no invisible overlays */
        [data-testid="stHorizontalBlock"] [data-testid="column"] {
            position: relative !important;
            z-index: 5 !important;
        }
        </style>
        
        <script>
        // Fix for button click issues - ensure they respond on first click
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(function() {
                const buttons = document.querySelectorAll('.stButton button');
                buttons.forEach(function(button) {
                    button.addEventListener('click', function(e) {
                        // Force the click to be recognized
                        e.stopPropagation();
                        this.click();
                    }, true);
                });
            }, 1000); // Wait for Streamlit to fully render
        });
        </script>
        """, unsafe_allow_html=True)
        
        # Use session state to make buttons more responsive
        if 'button_clicked' not in st.session_state:
            st.session_state.button_clicked = False
        
        # Two buttons side by side - Create Account and Login with improved response
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            create_account_clicked = st.button("Create Account", key="home_create_account_btn", use_container_width=True)
            if create_account_clicked and not st.session_state.button_clicked:
                st.session_state.button_clicked = True
                navigate_to("register")
        with btn_col2:
            login_clicked = st.button("Login", key="home_login_btn", use_container_width=True)
            if login_clicked and not st.session_state.button_clicked:
                st.session_state.button_clicked = True
                navigate_to("login")

    # Features section with Streamlit native components
    st.subheader("Why Choose Horizonite Bank?")
    
    # Create three columns for features
    feat_col1, feat_col2, feat_col3 = st.columns(3)
    
    # Custom CSS for feature cards
    st.markdown("""
    <style>
    .feature-card {
        background-color: #2d303e;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        text-align: center;
        height: 100%;
    }
    .feature-icon {
        width: 60px;
        height: 60px;
        margin: 0 auto 15px auto;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .secure-icon {
        background-color: rgba(61, 191, 255, 0.15);
        color: #3dbfff;
    }
    .transfer-icon {
        background-color: rgba(76, 175, 80, 0.15);
        color: #4CAF50;
    }
    .mobile-icon {
        background-color: rgba(255, 184, 0, 0.15);
        color: #FFB800;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Feature 1
    with feat_col1:
        st.markdown("""
        <div class="feature-card" style="border-top: 3px solid #3dbfff;">
            <div class="feature-icon secure-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#3dbfff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                </svg>
            </div>
            <h3 style="font-size: 20px; margin-bottom: 10px; color: #e4e6eb;">Secure Banking</h3>
            <p style="color: #a0a3ad; font-size: 15px;">Advanced encryption and authentication systems to keep your money and data safe.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Feature 2
    with feat_col2:
        st.markdown("""
        <div class="feature-card" style="border-top: 3px solid #4CAF50;">
            <div class="feature-icon transfer-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#4CAF50" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="12" y1="1" x2="12" y2="23"></line>
                    <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
                </svg>
            </div>
            <h3 style="font-size: 20px; margin-bottom: 10px; color: #e4e6eb;">Easy Transfers</h3>
            <p style="color: #a0a3ad; font-size: 15px;">Quick, hassle-free money transfers to any account with minimal fees.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Feature 3
    with feat_col3:
        st.markdown("""
        <div class="feature-card" style="border-top: 3px solid #FFB800;">
            <div class="feature-icon mobile-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#FFB800" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
                    <line x1="8" y1="21" x2="16" y2="21"></line>
                    <line x1="12" y1="17" x2="12" y2="21"></line>
                </svg>
            </div>
            <h3 style="font-size: 20px; margin-bottom: 10px; color: #e4e6eb;">Mobile Banking</h3>
            <p style="color: #a0a3ad; font-size: 15px;">Manage your finances anytime, anywhere with our easy-to-use platform.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Testimonials section - Convert to Streamlit native components
    st.subheader("What Our Customers Say")
    test_col1, test_col2 = st.columns(2)
    
    # Custom CSS for testimonials
    st.markdown("""
    <style>
    .testimonial-card {
        background-color: #2d303e;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        position: relative;
        height: 100%;
    }
    .testimonial-quote {
        font-size: 48px;
        position: absolute;
        top: 10px;
        left: 15px;
        opacity: 0.1;
    }
    .testimonial-content {
        color: #a0a3ad;
        font-size: 16px;
        margin-bottom: 20px;
        position: relative;
        z-index: 1;
    }
    .testimonial-author {
        display: flex;
        align-items: center;
    }
    .author-avatar {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 15px;
        font-weight: bold;
    }
    .author-info h4 {
        margin: 0;
        color: #e4e6eb;
        font-size: 16px;
    }
    .author-info p {
        margin: 0;
        color: #6b7280;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Testimonial 1
    with test_col1:
        st.markdown("""
        <div class="testimonial-card" style="border-left: 4px solid #3dbfff;">
            <div class="testimonial-quote" style="color: #3dbfff;">"</div>
            <p class="testimonial-content">Horizonite Bank has transformed how I manage my finances. Their intuitive platform and helpful customer service make banking a breeze.</p>
            <div class="testimonial-author">
                <div class="author-avatar" style="background-color: #3949AB;">RM</div>
                <div class="author-info">
                    <h4>Animesh Raj </h4>
                    <p>Business Owner</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Testimonial 2
    with test_col2:
        st.markdown("""
        <div class="testimonial-card" style="border-left: 4px solid #4CAF50;">
            <div class="testimonial-quote" style="color: #4CAF50;">"</div>
            <p class="testimonial-content">The EMI calculator and financial planning tools have helped me make informed decisions about my loans and investments.</p>
            <div class="testimonial-author">
                <div class="author-avatar" style="background-color: #4CAF50;">PS</div>
                <div class="author-info">
                    <h4>Kanchan Kumari</h4>
                    <p>IT Professional</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Call to action - Using Streamlit native components
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Add some spacing
    st.write("")
    
    # Pure Streamlit components for the call to action section
    cta_col1, cta_col2, cta_col3 = st.columns([1, 3, 1])
    with cta_col2:
        # Custom CSS for CTA section to apply gradient background
        st.markdown("""
        <style>
        .cta-container {
            background: linear-gradient(135deg, #3949AB 0%, #1E3A8A 100%);
            border-radius: 16px;
            padding: 40px 30px;
            margin-bottom: 30px;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
            text-align: center;
        }
        .cta-content {
            padding: 20px;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Container with content directly inside
        st.markdown("""
        <div class="cta-container">
            <div class="cta-content">
                <h2 style="font-size: 28px; margin-bottom: 15px;">Ready to Experience Better Banking?</h2>
                <p style="font-size: 16px; color: rgba(255, 255, 255, 0.9);">Join thousands of satisfied customers who have switched to Horizonite Bank for a more secure, convenient, and rewarding banking experience.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Add a simple footer with Streamlit native components
    st.write("")
    st.write("")
    
    footer_col1, footer_col2, footer_col3 = st.columns([1, 3, 1])
    with footer_col2:
        st.markdown("""
        <style>
        .footer-container {
            padding: 30px 0;
            text-align: center;
            border-top: 1px solid #3e4251;
            margin-top: 40px;
        }
        .footer-links {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-top: 15px;
        }
        .footer-link {
            color: #a0a3ad;
            text-decoration: none;
            font-size: 14px;
        }
        </style>
        
        <div class="footer-container">
            <p style="color: #6b7280; font-size: 14px;">© 2025 Horizonite Bank. All rights reserved.</p>
            <div class="footer-links">
                <a href="#" class="footer-link">Privacy Policy</a>
                <a href="#" class="footer-link">Terms of Service</a>
                <a href="#" class="footer-link">Contact Us</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Main app
def main():
    display_header()
    display_notification()
    display_sidebar()
    
    # Display the current page
    if not st.session_state.logged_in and st.session_state.current_page == "login":
        # Show the home page instead of the login page for new visitors
        if 'home_page_visited' not in st.session_state:
            st.session_state.current_page = "home"
            st.session_state.home_page_visited = True
    
    if st.session_state.current_page == "home":
        home_page()
    elif st.session_state.current_page == "login":
        login_page()
    elif st.session_state.current_page == "register":
        register_page()
    elif st.session_state.current_page == "dashboard":
        if not st.session_state.logged_in:
            navigate_to("login")
            show_notification("Please login to continue", "info")
        else:
            dashboard_page()
    elif st.session_state.current_page == "account_details":
        if not st.session_state.logged_in:
            navigate_to("login")
            show_notification("Please login to continue", "info")
        else:
            account_details_page()
    elif st.session_state.current_page == "transactions":
        if not st.session_state.logged_in:
            navigate_to("login")
            show_notification("Please login to continue", "info")
        else:
            transactions_page()
    elif st.session_state.current_page == "transfer":
        if not st.session_state.logged_in:
            navigate_to("login")
            show_notification("Please login to continue", "info")
        else:
            transfer_page()
    elif st.session_state.current_page == "emi_calculator":
        if not st.session_state.logged_in:
            navigate_to("login")
            show_notification("Please login to continue", "info")
        else:
            emi_calculator_page()

if __name__ == "__main__":
    main()
