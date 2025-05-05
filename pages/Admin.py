import streamlit as st
# Set page to wide mode - must be first Streamlit command
try:
    st.set_page_config(layout="wide", page_title="Admin Panel")
except:
    # This may fail if the page config was already set, which is fine
    pass

import pandas as pd
from datetime import datetime, timedelta
import json
import os
import json
# Handle missing utils module gracefully
try:
    from utils.db import get_all_users
except ModuleNotFoundError:
    # Define a fallback function if the module is missing
    def get_all_users():
        return {}  # Return empty data
    
import plotly.express as px

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
ACCOUNTS_FILE = os.path.join(DATA_DIR, 'accounts.json')
TRANSACTIONS_FILE = os.path.join(DATA_DIR, 'transactions.json')
CONTACT_MESSAGES_FILE = os.path.join(DATA_DIR, 'contact_messages.json')

# Initialize session state for login persistence
if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False

def load_json_data(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        st.error(f"Error decoding JSON from {os.path.basename(file_path)}")
        return {}

def save_json_data(file_path, data):
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        return True, "Data saved successfully"
    except Exception as e:
        return False, f"Error saving data: {e}"

# Predefined admin credentials
ADMIN_CREDENTIALS = {
    "ani": "123",
     "arya": "118251",
   
}

def show_login_form():
    st.subheader("Admin Login")
    with st.form("admin_login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            if email in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[email] == password:
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("Invalid email or password")

def show_admin_page():
    # Add custom CSS to provide more spacing above the title
    st.markdown("""
    <style>
    .main > div:first-child {
        padding-top: 30px;
    }
    div[data-testid="stAppViewBlockContainer"] > div:first-child {
        margin-top: 20px;
    }
    h1:first-of-type {
        margin-top: 20px;
        padding-top: 20px;
        font-size: 36px;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Add some vertical space before the title
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    st.title("Admin Panel")

    if st.session_state.admin_logged_in:
        # Logout button
        if st.sidebar.button("Logout"):
            st.session_state.admin_logged_in = False
            st.rerun()
        
        # Display admin panel content
        show_admin_panel_content()
    else:
        show_login_form()

def show_admin_panel_content():
    # Add CSS for better tab styling
    st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        white-space: pre-wrap;
        font-size: 28px;
        font-weight: 900;
        background-color: #262730;
        border-radius: 4px;
        padding: 5px 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        min-width: 200px;
        max-width: 250px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4F4FD3 !important;
        color: white !important;
    }
    /* Custom styling for tab text */
    .stTabs [data-baseweb="tab-highlight"] {
        display: none;
    }
    .stTabs [data-baseweb="tab"] [data-testid="stMarkdownContainer"] p {
        font-weight: 900;
        margin: 0;
        padding: 0;
        line-height: 1;
        transform: scale(1.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create tabs for different admin functions with larger font and better styling
    tab1, tab2, tab3 = st.tabs(["User Management", "Transaction Monitoring", "Contact Messages"])
    
    with tab1:
        show_user_management()
    
    with tab2:
        show_transaction_monitoring()
        
    with tab3:
        show_contact_messages()

def show_user_management():
    # Import pandas locally to ensure it's available in this function
    import pandas as pd
    
    # Add enhanced styling for user management section
    st.markdown("""
    <style>
    /* User Management Section Styling */
    .user-management-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
    }
    .user-management-title {
        font-size: 24px;
        font-weight: 600;
        color: #ffffff;
        margin: 0;
    }
    .user-card {
        background-color: #1E1E1E;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border-left: 4px solid #4F4FD3;
    }
    .user-metrics {
        display: flex;
        gap: 15px;
        margin-bottom: 20px;
        flex-wrap: nowrap;
        overflow-x: auto;
        white-space: nowrap;
        padding-bottom: 10px;
    }
    .metric-card {
        background-color: #1e1e2d;
        border-radius: 8px;
        padding: 20px 25px;
        flex: 1 0 auto; /* Don't shrink, grow if possible, start at auto */
        min-width: 200px; /* Minimum width to prevent excessive narrowing */
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-card.green {
        border-left: 5px solid #4CAF50;
    }
    .metric-card.red {
        border-left: 5px solid #F44336;
    }
    .metric-card h4 {
        margin: 0;
        color: #ffffff;
        font-size: 18px;
        font-weight: 500;
    }
    .metric-card p {
        margin: 15px 0 0 0;
        font-size: 28px;
        font-weight: bold;
        color: #ffffff;
    }
    .user-filters {
        background-color: #262730;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px;
    }
    .user-table {
        background-color: #1E1E1E;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 30px;
    }
    .user-details-container {
        display: flex;
        gap: 20px;
    }
    .user-profile {
        background-color: #1E1E1E;
        border-radius: 8px;
        padding: 20px;
        width: 100%;
    }
    .user-avatar {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        background-color: #4F4FD3;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 20px;
        font-size: 40px;
        color: white;
        font-weight: bold;
    }
    .profile-header {
        text-align: center;
        margin-bottom: 30px;
    }
    .profile-header h3 {
        margin: 10px 0;
        font-size: 22px;
        font-weight: 600;
    }
    .profile-header p {
        margin: 0;
        color: #AAAAAA;
        font-size: 15px;
    }
    .profile-section {
        margin-bottom: 25px;
    }
    .profile-section h4 {
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 15px;
        color: #CCCCCC;
        border-bottom: 1px solid #333333;
        padding-bottom: 8px;
    }
    .profile-field {
        display: flex;
        margin-bottom: 12px;
    }
    .field-label {
        flex: 0 0 120px;
        color: #AAAAAA;
        font-size: 14px;
    }
    .field-value {
        flex: 1;
        font-size: 14px;
        font-weight: 500;
    }
    .action-buttons {
        display: flex;
        gap: 15px;
        margin-top: 20px;
    }
    .action-button {
        flex: 1;
        text-align: center;
        padding: 10px;
        border-radius: 5px;
        font-weight: 500;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .action-button.primary {
        background-color: #4F4FD3;
        color: white;
    }
    .action-button.danger {
        background-color: #E53935;
        color: white;
    }
    .action-button.secondary {
        background-color: #333333;
        color: white;
    }
    .status-badge {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: 500;
    }
    .status-active {
        background-color: #4CAF50;
        color: white;
    }
    .status-blocked {
        background-color: #F44336;
        color: white;
    }
    .status-pending {
        background-color: #FF9800;
        color: white;
    }
    .search-box {
        background-color: #262730;
        border-radius: 8px;
        padding: 15px 20px;
        margin-bottom: 20px;
    }
    /* Styling for the data table control buttons */
    .stButton > button {
        background-color: #2e3346;
        color: white;
        border: 1px solid #3e4251;
        border-radius: 6px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #4F4FD3;
        border-color: #4F4FD3;
        transform: translateY(-2px);
    }
    /* Buttons that already have a primary style */
    button[kind="primary"] {
        background-color: #4F4FD3 !important;
        border-color: #4F4FD3 !important;
    }
    /* Add styles for the full-screen mode */
    .dataframe-fullscreen {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 9999;
        background-color: #1a1c23;
        padding: 20px;
        overflow: auto;
    }
    /* Style for print view */
    @media print {
        body * {
            visibility: hidden;
        }
        .user-table, .user-table * {
            visibility: visible;
        }
        .user-table {
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
        }
        /* Hide elements not needed in print */
        .stButton, .stSelectbox, .stDownloadButton {
            display: none !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # Header with metrics
    st.markdown('<div class="user-management-header">', unsafe_allow_html=True)
    st.markdown('<h2 class="user-management-title">User Management</h2>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Load data directly from JSON files
    users_data = load_json_data(USERS_FILE)
    accounts_data = load_json_data(ACCOUNTS_FILE)

    if not users_data:
        st.info("No users found in users.json")
        return

    # Create a list of user summaries
    user_summaries = []
    for user_id, user_info in users_data.items():
        # Get account balance from accounts_data
        balance = 0
        account_info = accounts_data.get(user_id)
        if account_info:
            balance = account_info.get("balance", 0)

        # Create user summary
        user_summary = {
            "user_id": user_id,
            "name": user_info.get("full_name", ""),
            "email": user_info.get("email", ""),
            "phone": user_info.get("phone", ""),
            "balance": balance,
            "status": user_info.get("status", "Active"), # Assuming status is stored in users.json
            "created_at": user_info.get("created_at", "")
        }
        user_summaries.append(user_summary)

    # Create DataFrame for display
    df = pd.DataFrame(user_summaries)

    # Show metrics in a single row
    cols = st.columns(4)
    
    # Total users metric
    with cols[0]:
        st.markdown(f"""
        <div class="metric-card green">
            <h4>Total Users</h4>
            <p>{len(user_summaries)}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Active users metric
    active_users = len([u for u in user_summaries if u["status"] == "Active"])
    with cols[1]:
        st.markdown(f"""
        <div class="metric-card green">
            <h4>Active Users</h4>
            <p>{active_users}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Blocked users metric
    blocked_users = len([u for u in user_summaries if u["status"] == "Blocked"])
    with cols[2]:
        st.markdown(f"""
        <div class="metric-card red">
            <h4>Blocked Users</h4>
            <p>{blocked_users}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Total balance metric
    total_balance = sum([u["balance"] for u in user_summaries])
    with cols[3]:
        st.markdown(f"""
        <div class="metric-card green">
            <h4>Total Balance</h4>
            <p>₹{total_balance:,.2f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Search and filter section
    st.markdown('<div class="search-box">', unsafe_allow_html=True)
    search_col1, search_col2 = st.columns([3, 1])
    
    with search_col1:
        search_query = st.text_input("Search users by name, email or phone", placeholder="Type to search...")
    
    with search_col2:
        status_filter = st.selectbox("Status", ["All", "Active", "Blocked"])
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Format the DataFrame
    if not df.empty:
        # Ensure 'created_at' exists and handle potential errors
        if 'created_at' in df.columns:
            df["created_at_dt"] = pd.to_datetime(df["created_at"], errors='coerce')
            df["joined_date"] = df["created_at_dt"].dt.strftime("%Y-%m-%d")
        else:
            df["joined_date"] = "N/A"
            
        df["balance_formatted"] = df["balance"].apply(lambda x: f"₹{x:,.2f}")
        
        # Apply search filter if provided
        if search_query:
            # Apply the search filter across name, email, and phone
            df = df[
                df["name"].str.contains(search_query, case=False, na=False) |
                df["email"].str.contains(search_query, case=False, na=False) |
                df["phone"].str.contains(search_query, case=False, na=False)
            ]
        
        # Apply status filter if not "All"
        if status_filter != "All":
            df = df[df["status"] == status_filter]

        # Display users in a table with improved styling
        st.markdown('<div class="user-table">', unsafe_allow_html=True)
        st.markdown(f"<p style='margin-bottom:15px;'>Showing {len(df)} users</p>", unsafe_allow_html=True)
        
        # Add table controls with action buttons for export, full screen, etc.
        control_col1, control_col2, control_col3, control_col4, control_col5 = st.columns([1, 1, 1, 1, 1])
        
        with control_col1:
            # Export to CSV button
            if st.button("📥 Export to CSV", key="export_csv", use_container_width=True):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="user_data.csv",
                    mime="text/csv",
                    key="download_csv"
                )
        
        with control_col2:
            # Refresh button
            if st.button("🔄 Refresh Data", key="refresh_data", use_container_width=True):
                st.rerun()
        
        with control_col3:
            # Toggle view mode (compact/expanded)
            if 'expanded_view' not in st.session_state:
                st.session_state.expanded_view = False
            
            if st.button(
                "🔍 " + ("Compact View" if st.session_state.expanded_view else "Expanded View"), 
                key="toggle_view",
                use_container_width=True
            ):
                st.session_state.expanded_view = not st.session_state.expanded_view
        
        with control_col4:
            # Print button that uses browser's print functionality
            if st.button("🖨️ Print Table", key="print_table", use_container_width=True):
                st.markdown("""
                <script>
                    // Add a small delay to ensure the table is rendered
                    setTimeout(function() {
                        window.print();
                    }, 1000);
                </script>
                """, unsafe_allow_html=True)
        
        with control_col5:
            # Bulk actions dropdown
            bulk_action = st.selectbox(
                "Bulk Actions",
                ["Select Action", "Block Selected", "Activate Selected", "Delete Selected"],
                key="bulk_action"
            )
            
            if bulk_action != "Select Action":
                if st.button("Apply", key="apply_bulk_action"):
                    st.warning(f"Implementation of '{bulk_action}' would go here")
        
        # Create a function to map status to colors
        def get_status_color(status):
            status = status.lower() if status else ""
            if status == "active":
                return "#4CAF50"  # Green for active
            elif status == "blocked" or status == "inactive":
                return "#E53935"  # Red for blocked/inactive
            elif status == "pending":
                return "#FFC107"  # Yellow for pending
            else:
                return "#9E9E9E"  # Grey for other statuses
        
        # Add status color column
        df["_status_color"] = df["status"].apply(get_status_color)
        
        # Display the table with better styling - don't use HTML in dataframe
        try:
            # Determine table height based on view mode
            table_height = 600 if st.session_state.expanded_view else 400
            
            # Try to use BadgeColumn if available (newer Streamlit versions)
            st.dataframe(
                df[["name", "email", "phone", "balance_formatted", "status", "joined_date"]], 
                height=table_height, 
                use_container_width=True,
                hide_index=True,
                column_config={
                    "name": "Name",
                    "email": "Email",
                    "phone": "Phone",
                    "balance_formatted": "Balance",
                    "status": st.column_config.BadgeColumn(
                        "Status",
                        help="User account status",
                        width="medium",
                        # Map status values to badge colors
                        map_badge={
                            "active": "success", 
                            "Active": "success",
                            "blocked": "danger",
                            "Blocked": "danger", 
                            "inactive": "danger", 
                            "Inactive": "danger",
                            "pending": "warning",
                            "Pending": "warning"
                        }
                    ),
                    "joined_date": "Joined On"
                }
            )
            
            # Add fullscreen button 
            fullscreen_col1, fullscreen_col2 = st.columns([4, 1])
            with fullscreen_col2:
                if st.button("🖥️ Full Screen", key="fullscreen_button"):
                    # Use JavaScript via HTML to request fullscreen
                    st.markdown("""
                    <script>
                        // Try to find the dataframe element
                        const dataframeElement = window.parent.document.querySelector('[data-testid="stDataFrame"]');
                        if (dataframeElement) {
                            try {
                                if (dataframeElement.requestFullscreen) {
                                    dataframeElement.requestFullscreen();
                                } else if (dataframeElement.mozRequestFullScreen) { /* Firefox */
                                    dataframeElement.mozRequestFullScreen();
                                } else if (dataframeElement.webkitRequestFullscreen) { /* Chrome, Safari & Opera */
                                    dataframeElement.webkitRequestFullscreen();
                                } else if (dataframeElement.msRequestFullscreen) { /* IE/Edge */
                                    dataframeElement.msRequestFullscreen();
                                }
                            } catch (e) {
                                console.error("Fullscreen request failed:", e);
                            }
                        }
                    </script>
                    """, unsafe_allow_html=True)
            
            # Add export to Excel option
            with fullscreen_col1:
                if st.button("📊 Export to Excel", key="export_excel", use_container_width=True):
                    # Create a BytesIO object to store the Excel file
                    try:
                        import io
                        try:
                            # Try to use xlsxwriter for better formatting
                            from xlsxwriter import Workbook
                            
                            buffer = io.BytesIO()
                            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                                df.to_excel(writer, sheet_name='Users', index=False)
                                workbook = writer.book
                                worksheet = writer.sheets['Users']
                                
                                # Add some formatting
                                header_format = workbook.add_format({
                                    'bold': True, 
                                    'fg_color': '#4F4FD3', 
                                    'border': 1,
                                    'font_color': 'white'
                                })
                                
                                # Write the column headers with the defined format
                                for col_num, value in enumerate(df.columns.values):
                                    worksheet.write(0, col_num, value, header_format)
                                    worksheet.set_column(col_num, col_num, 15)
                        except ImportError:
                            # Fallback to basic Excel export if xlsxwriter is not available
                            buffer = io.BytesIO()
                            df.to_excel(buffer, index=False)
                        
                        # Reset buffer position
                        buffer.seek(0)
                        
                        # Offer the Excel file for download
                        st.download_button(
                            label="Download Excel",
                            data=buffer,
                            file_name="user_data.xlsx",
                            mime="application/vnd.ms-excel",
                            key="download_excel"
                        )
                    except Exception as e:
                        st.error(f"Error exporting to Excel: {e}")
        
        except (AttributeError, TypeError):
            # Fallback for older Streamlit versions without BadgeColumn
            st.dataframe(
                df[["name", "email", "phone", "balance_formatted", "status", "joined_date"]], 
                height=table_height, 
                use_container_width=True,
                hide_index=True,
                column_config={
                    "name": "Name",
                    "email": "Email",
                    "phone": "Phone",
                    "balance_formatted": "Balance",
                    "status": st.column_config.TextColumn(
                        "Status",
                        help="User account status",
                        width="medium",
                    ),
                    "joined_date": "Joined On"
                }
            )
            
            # For older Streamlit versions, still provide export and fullscreen options
            fullscreen_col1, fullscreen_col2 = st.columns([4, 1])
            with fullscreen_col2:
                if st.button("🖥️ Full Screen", key="fullscreen_button_fallback"):
                    st.warning("Full screen may not be supported in this version of Streamlit")
            
            with fullscreen_col1:
                if st.button("📊 Export to Excel", key="export_excel_fallback", use_container_width=True):
                    try:
                        import io
                        
                        # Simple Excel export without formatting
                        buffer = io.BytesIO()
                        
                        # Ensure pandas is available in this scope
                        import pandas as pd
                        
                        df.to_excel(buffer, index=False)
                        buffer.seek(0)
                        
                        st.download_button(
                            label="Download Excel",
                            data=buffer,
                            file_name="user_data.xlsx",
                            mime="application/vnd.ms-excel"
                        )
                    except Exception as e:
                        st.error(f"Error exporting to Excel: {e}")
        
        st.markdown('</div>', unsafe_allow_html=True)

        # User details section with improved layout
        st.subheader("User Details")
        
        # Add user search bar for the details section
        user_search = st.text_input("Search for user by name, email or ID", key="user_detail_search", placeholder="Start typing to search...")
        
        # User selection with better UX
        user_options = [f"{users_data.get(uid, {}).get('full_name', 'Unknown')} ({users_data.get(uid, {}).get('email', uid)})" 
                        for uid in users_data.keys()]
        user_ids = list(users_data.keys())
        
        if not user_ids:
            st.warning("No users available for selection.")
            return
            
        # Create a mapping from display name to user_id
        user_display_to_id = {f"{users_data.get(uid, {}).get('full_name', 'Unknown')} ({users_data.get(uid, {}).get('email', uid)})": uid 
                            for uid in users_data.keys()}
        
        # Filter user options based on search query
        if user_search:
            filtered_options = [opt for opt in user_options if user_search.lower() in opt.lower()]
            if not filtered_options and filtered_options != user_options:
                st.info(f"No users found matching '{user_search}'. Showing all users.")
                filtered_options = user_options
        else:
            filtered_options = user_options
        
        selected_user_display = st.selectbox(
            "Select User",
            options=filtered_options,
            key="user_detail_select"
        )
        
        selected_user_id = user_display_to_id.get(selected_user_display)

        if selected_user_id:
            user_data = users_data.get(selected_user_id)
            account_data = accounts_data.get(selected_user_id)

            if user_data:
                # Improved user details display with visual enhancements
                st.markdown('<div class="user-profile">', unsafe_allow_html=True)
                
                # Profile header with avatar
                st.markdown('<div class="profile-header">', unsafe_allow_html=True)
                # Generate avatar with user's initials
                name = user_data.get('full_name', 'Unknown User')
                initials = ''.join([n[0].upper() for n in name.split(' ')[:2]]) if name else 'U'
                st.markdown(f'<div class="user-avatar">{initials}</div>', unsafe_allow_html=True)
                
                # Display name and status
                status = user_data.get("status", "Active")
                status_class = f"status-{status.lower()}"
                st.markdown(f'<h3>{name}</h3>', unsafe_allow_html=True)
                st.markdown(f'<p>{user_data.get("email", "")}</p>', unsafe_allow_html=True)
                st.markdown(f'<span class="status-badge {status_class}">{status}</span>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Two column layout for user details
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown('<div class="profile-section">', unsafe_allow_html=True)
                    st.markdown('<h4>Personal Information</h4>', unsafe_allow_html=True)
                    
                    # Create field rows
                    fields = [
                        ("Full Name", user_data.get('full_name', 'N/A')),
                        ("Email", user_data.get('email', 'N/A')),
                        ("Phone", user_data.get('phone', 'N/A')),
                        ("Date of Birth", user_data.get('dob', 'N/A')),
                        ("PAN", user_data.get('pan', 'N/A')),
                        ("Aadhar", user_data.get('aadhar', 'N/A')),
                        ("Address", user_data.get('address', 'N/A')),
                    ]
                    
                    for label, value in fields:
                        st.markdown(f"""
                        <div class="profile-field">
                            <div class="field-label">{label}:</div>
                            <div class="field-value">{value}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)

                with col2:
                    st.markdown('<div class="profile-section">', unsafe_allow_html=True)
                    st.markdown('<h4>Account Information</h4>', unsafe_allow_html=True)
                    
                    if account_data:
                        account_fields = [
                            ("Account Number", account_data.get('account_number', 'N/A')),
                            ("Account Type", account_data.get('account_type', 'N/A')),
                            ("Balance", f"₹{account_data.get('balance', 0):,.2f}"),
                            ("Status", account_data.get('status', 'N/A')),
                            ("Created At", account_data.get('created_at', 'N/A')),
                        ]
                        
                        for label, value in account_fields:
                            st.markdown(f"""
                            <div class="profile-field">
                                <div class="field-label">{label}:</div>
                                <div class="field-value">{value}</div>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.markdown("<p>No account information found.</p>", unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Activity section
                st.markdown('<div class="profile-section">', unsafe_allow_html=True)
                st.markdown('<h4>User Activity</h4>', unsafe_allow_html=True)
                
                # Show mock or real activity data if available
                st.markdown('<p>Last login: Today at 10:45 AM</p>', unsafe_allow_html=True)
                st.markdown('<p>Recent transactions: 5 transactions in last 7 days</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # User actions with improved buttons
                st.markdown('<div class="profile-section">', unsafe_allow_html=True)
                st.markdown('<h4>User Actions</h4>', unsafe_allow_html=True)
                
                st.markdown('<div class="action-buttons">', unsafe_allow_html=True)
                
                current_status = user_data.get("status", "Active")
                if current_status == "Blocked":
                    if st.button("Unblock User", key="unblock_user", use_container_width=True):
                        users_data[selected_user_id]["status"] = "Active"
                        success, message = save_json_data(USERS_FILE, users_data)
                        if success:
                            st.success("User unblocked successfully")
                            st.rerun()
                        else:
                            st.error(message)
                else:
                    if st.button("Block User", key="block_user", use_container_width=True):
                        users_data[selected_user_id]["status"] = "Blocked"
                        success, message = save_json_data(USERS_FILE, users_data)
                        if success:
                            st.success("User blocked successfully")
                            st.rerun()
                        else:
                            st.error(message)
                
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)

def show_transaction_monitoring():
    st.subheader("Transaction Monitoring")
    
    # Load transaction data directly from JSON file
    all_transactions_dict = load_json_data(TRANSACTIONS_FILE)
    users_data = load_json_data(USERS_FILE) # Need user data for names
    accounts_data = load_json_data(ACCOUNTS_FILE) # Load account data for account numbers

    if not all_transactions_dict:
        st.info("No transactions found in transactions.json")
        return

    processed_transactions = []
    # Assuming transactions_data structure is {user_id: [ {id, type, amount, description, timestamp}, ... ]}
    for user_id, tx_list in all_transactions_dict.items():
        if not isinstance(tx_list, list):
            continue
        for tx in tx_list:
            tx_copy = tx.copy()
            # Map fields
            tx_copy['transaction_id'] = tx_copy.get('id', '')
            tx_copy['user_id'] = user_id
            user_info = users_data.get(user_id, {})
            tx_copy['user_name'] = user_info.get('full_name', 'Unknown User')
            # Add account number from accounts.json
            account_info = accounts_data.get(user_id, {})
            tx_copy['account_number'] = account_info.get('account_number', 'N/A')
            # Ensure other essential fields have defaults
            tx_copy.setdefault('type', 'N/A')
            tx_copy.setdefault('amount', 0)
            tx_copy.setdefault('description', 'N/A')
            tx_copy.setdefault('timestamp', None)
            processed_transactions.append(tx_copy)

    if not processed_transactions:
        st.info("No transactions available to display.")
        return

    # Create DataFrame for display
    df = pd.DataFrame(processed_transactions)
    # Map actual account numbers from accounts_data into DataFrame
    df['account_number'] = df['user_id'].apply(lambda uid: accounts_data.get(uid, {}).get('account_number', 'N/A'))

    # Post-processing checks for DataFrame (optional but safer)
    if df.empty:
        st.info("No processable transactions found.")
        return

    # Ensure essential columns exist after DataFrame creation, assign defaults if needed
    for col in ['transaction_id', 'user_name', 'account_number', 'type', 'description']:
        if col not in df.columns: df[col] = 'N/A'
    if 'amount' not in df.columns: df['amount'] = 0
    if 'timestamp' not in df.columns: df['timestamp'] = pd.NaT # Use NaT for missing timestamps
    
    # Format the DataFrame
    if not df.empty:
        # Add custom CSS to make better use of space
        st.markdown("""
        <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
            margin-top: 0px;
            max-width: 100% !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        .element-container {
            margin-bottom: 0.5rem;
        }
        .stDataFrame {
            height: 650px;
            overflow: auto;
            width: 100% !important;
        }
        .stDataFrame [data-testid="stDataFrameResizable"] {
            width: 100% !important;
            max-width: none !important;
        }
        /* Stat cards styling */
        .stat-card-container {
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
        }
        .stat-card {
            flex: 1;
            padding: 20px 25px;
            border-radius: 8px;
            background-color: #262730;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border-left: 5px solid #4CAF50;
        }
        .stat-card.debit {
            border-left: 5px solid #F44336;
        }
        .stat-card h4 {
            margin: 0;
            color: #ffffff;
            font-size: 18px;
            font-weight: 500;
        }
        .stat-card p {
            margin: 10px 0 0 0;
            font-size: 28px;
            font-weight: bold;
            color: #ffffff;
        }
        /* Analytics container */
        .analytics-container {
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
        }
        .chart-container {
            flex: 1;
            background-color: #1E1E1E;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .section-header {
            font-size: 24px;
            font-weight: 600;
            margin-top: 30px;
            margin-bottom: 20px;
            color: #ffffff;
        }
        /* Tab styling */
        div[data-testid="stHorizontalBlock"] {
            gap: 0px !important;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 0px;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 10px 24px;
            background-color: #2C2C3C;
        }
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background-color: #4F4FD3 !important;
            color: white !important;
        }
        /* Filter section */
        .filter-section {
            background-color: #1E1E1E;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }
        /* Sort panel styling */
        .sort-panel {
            background-color: #1E1E1E;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
        }
        /* Styling for labels */
        .sort-label {
            color: #7f8fa6 !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            margin-bottom: 8px !important;
        }
        /* Dropdown styling */
        .stSelectbox [data-baseweb="select"] {
            background-color: #232838 !important;
            border-radius: 4px !important;
            border: none !important;
            padding: 5px !important;
        }
        .stSelectbox [data-baseweb="select"] div {
            background-color: #232838 !important;
            color: white !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["date"] = df["timestamp"].dt.strftime("%Y-%m-%d %H:%M")
        df["amount_formatted"] = df.apply(
            lambda row: f"+₹{row['amount']:,.2f}" if row["type"] == "credit" else f"-₹{row['amount']:,.2f}",
            axis=1
        )
        
        # Sort by timestamp (newest first)
        df = df.sort_values("timestamp", ascending=False)
        
        # Add summary statistics at the top
        total_transactions = len(df)
        total_credit = df[df["type"] == "credit"]["amount"].sum()
        total_debit = df[df["type"] == "debit"]["amount"].sum()
        
        # Use HTML for the stat cards to ensure consistent layout
        st.markdown(f"""
        <div class="stat-card-container">
            <div class="stat-card">
                <h4>Total Transactions</h4>
                <p>{total_transactions}</p>
            </div>
            <div class="stat-card">
                <h4>Total Credits</h4>
                <p>₹{total_credit:,.2f}</p>
            </div>
            <div class="stat-card debit">
                <h4>Total Debits</h4>
                <p>₹{total_debit:,.2f}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Transaction Details section
        st.markdown('<div class="section-header">Transaction Details</div>', unsafe_allow_html=True)
        
        # Create a filter section with better styling
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        # Filter section - place it above the analytics
        filter_col1, filter_col2, filter_col3 = st.columns([1, 1, 1])
        with filter_col1:
            # Date range filter
            date_range = st.selectbox(
                "Date Range",
                ["All Time", "Today", "Last 7 Days", "Last 30 Days", "Custom"]
            )
            
            if date_range == "Custom":
                date_cols = st.columns(2)
                with date_cols[0]:
                    start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
                with date_cols[1]:
                    end_date = st.date_input("End Date", datetime.now())
            else:
                # Set date range based on selection
                end_date = datetime.now()
                if date_range == "Today":
                    start_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0)
                elif date_range == "Last 7 Days":
                    start_date = end_date - timedelta(days=7)
                elif date_range == "Last 30 Days":
                    start_date = end_date - timedelta(days=30)
                else:  # All Time
                    start_date = datetime.min
        
        with filter_col2:
            # Transaction type filter
            transaction_type = st.selectbox(
                "Transaction Type",
                ["All", "Credit", "Debit"]
            )

        with filter_col3:
            # Amount min/max in single row
            amount_cols = st.columns(2)
            with amount_cols[0]:
                min_amount = st.number_input("Min Amount", min_value=0.0, step=1000.0)
            with amount_cols[1]:
                max_amount = st.number_input("Max Amount", min_value=0.0, step=1000.0)
                
        # Apply filter button
        if st.button("Apply Filters", key="apply_filters"):
            st.session_state.filters_applied = True
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Transaction Analytics Section with better HTML structure
        st.markdown('<div class="section-header">Transaction Analytics</div>', unsafe_allow_html=True)
        
        if not df.empty:
            # Generate mock data if there's no actual transaction data
            # This ensures charts always display something even during testing
            if len(df) < 2 or df["type"].nunique() < 2:
                # Create mock data for demonstration
                mock_data = {'type': ['credit', 'debit'], 'amount': [100000, 10000]}
                type_summary = pd.DataFrame(mock_data)
                
                # Create mock date summary
                dates = [(datetime.now() - timedelta(days=i)).date() for i in range(7)]
                mock_dates = []
                for d in dates:
                    mock_dates.append({'date_only': d, 'type': 'credit', 'amount': 100000 - (i * 10000)})
                    mock_dates.append({'date_only': d, 'type': 'debit', 'amount': 10000 - (i * 1000)})
                date_summary = pd.DataFrame(mock_dates)
            else:
                # Group by date and type
                df["date_only"] = df["timestamp"].dt.date
                
                # Create summary by type
                type_summary = df.groupby("type")["amount"].sum().reset_index()
                
                # Create summary by date
                date_summary = df.groupby(["date_only", "type"])["amount"].sum().reset_index()
            
            st.markdown('<div class="analytics-container">', unsafe_allow_html=True)
            
            # Use columns within the analytics container for the charts
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                # Pie chart
                fig1 = px.pie(
                    type_summary, 
                    values="amount", 
                    names="type",
                    title="Credit vs Debit",
                    color="type",
                    color_discrete_map={"credit": "#4CAF50", "debit": "#F44336"}
                )
                fig1.update_traces(textposition='inside', textinfo='percent+label')
                fig1.update_layout(
                    margin=dict(t=40, b=20, l=20, r=20), 
                    height=350,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#CCCCCC', size=14),
                    title_font=dict(size=20),
                    showlegend=True,
                    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
                )
                st.plotly_chart(fig1, use_container_width=True)
            
            with chart_col2:
                # Line chart
                fig2 = px.line(
                    date_summary,
                    x="date_only",
                    y="amount",
                    color="type",
                    title="Transaction History",
                    color_discrete_map={"credit": "#4CAF50", "debit": "#F44336"}
                )
                fig2.update_layout(
                    xaxis_title="Date", 
                    yaxis_title="Amount (₹)",
                    margin=dict(t=40, b=20, l=20, r=20),
                    height=350,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#CCCCCC', size=14),
                    title_font=dict(size=20),
                    showlegend=True,
                    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
                )
                st.plotly_chart(fig2, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

        # Transaction List Section
        st.markdown('<div class="section-header">Transaction List</div>', unsafe_allow_html=True)
        st.markdown('<div style="background-color:#1E1E1E; padding:20px; border-radius:8px; box-shadow:0 4px 10px rgba(0,0,0,0.15);">', unsafe_allow_html=True)
        
        # Filter transactions based on selected filters
        filtered_df = df.copy()
        
        # Apply date filter
        if date_range != "All Time":
            start_datetime = datetime.combine(start_date, datetime.min.time())
            end_datetime = datetime.combine(end_date, datetime.max.time())
            filtered_df = filtered_df[(filtered_df["timestamp"] >= start_datetime) & (filtered_df["timestamp"] <= end_datetime)]
        
        # Apply transaction type filter
        if transaction_type != "All":
            filtered_df = filtered_df[filtered_df["type"].str.lower() == transaction_type.lower()]
        
        # Apply amount filter
        if min_amount > 0:
            filtered_df = filtered_df[filtered_df["amount"] >= min_amount]
        
        if max_amount > 0:
            filtered_df = filtered_df[filtered_df["amount"] <= max_amount]
        
        # Display transactions in a card
        if filtered_df.empty:
            st.info("No transactions found matching the filters")
        else:
            st.markdown(f"<p style='margin-bottom:15px; font-size:18px;'>Showing {len(filtered_df)} transactions</p>", unsafe_allow_html=True)
            
            # Add sorting options
            st.markdown('<div class="sort-panel">', unsafe_allow_html=True)
            sort_col1, sort_col2, sort_col3 = st.columns([1, 1, 1])
            
            with sort_col1:
                st.markdown('<p class="sort-label">Sort By</p>', unsafe_allow_html=True)
                sort_field = st.selectbox(
                    "",
                    options=["date", "amount", "name", "account", "type", "description"],
                    index=0
                )
                
            with sort_col2:
                st.markdown('<p class="sort-label">Sort Order</p>', unsafe_allow_html=True)
                sort_order = st.radio(
                    "",
                    options=["Descending", "Ascending"],
                    index=0,
                    horizontal=True
                )
                
            with sort_col3:
                st.markdown('<p class="sort-label">Amount Range</p>', unsafe_allow_html=True)
                sort_filter = st.radio(
                    "",
                    options=["All", "Highest", "Lowest"],
                    index=0,
                    horizontal=True
                )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Apply sorting based on user selections
            if sort_field == "amount":
                # Strip the '+₹' or '-₹' prefix from the amount_formatted for sorting
                filtered_df['sort_amount'] = filtered_df['amount']
                sort_col = 'sort_amount'
            elif sort_field == "date":
                sort_col = 'timestamp'
            else:
                # For other fields, use the display columns
                sort_col = {
                    "name": "user_name",
                    "account": "account_number",
                    "type": "type",
                    "description": "description"
                }.get(sort_field, "timestamp")
            
            # Apply sort direction
            ascending = sort_order == "Ascending"
            
            # Apply special filters (if selected)
            if sort_filter == "Highest" and len(filtered_df) > 0:
                # Sort by amount descending
                filtered_df = filtered_df.sort_values(by='amount', ascending=False).head(20)
            elif sort_filter == "Lowest" and len(filtered_df) > 0:
                # Sort by amount ascending
                filtered_df = filtered_df.sort_values(by='amount', ascending=True).head(20)
            else:
                # If "All" or any other option, just apply the regular sort
                filtered_df = filtered_df.sort_values(by=sort_col, ascending=ascending)
            
            # Display transactions in a table with increased height
            st.markdown('<div style="background-color:#1E1E1E; padding:15px; border-radius:8px; box-shadow:0 4px 10px rgba(0,0,0,0.15);">', unsafe_allow_html=True)
            # Prepare simplified columns for display to match the screenshot
            display_df = filtered_df[["user_name", "account_number", "type", "amount_formatted", "description", "date"]].rename(
                columns={
                    "user_name": "name",
                    "account_number": "account",
                    "type": "type",
                    "amount_formatted": "amount",
                    "description": "description",
                    "date": "date"
                }
            )
            
            st.dataframe(
                display_df,
                height=600,
                use_container_width=True,
                hide_index=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Flag suspicious transactions
            st.markdown('<div class="section-header">Suspicious Transactions</div>', unsafe_allow_html=True)
            
            # Find large transactions (over ₹50,000)
            large_transactions = filtered_df[filtered_df["amount"] > 50000]
            
            if large_transactions.empty:
                st.markdown('<div style="background-color:#1E1E1E; padding:20px; border-radius:8px; box-shadow:0 4px 10px rgba(0,0,0,0.15); text-align:center; margin-top:10px;">', unsafe_allow_html=True)
                st.markdown('<p style="font-size:18px; color:#4E5969; margin:0;">No suspicious transactions found</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="background-color:#1E1E1E; padding:15px; border-radius:8px; box-shadow:0 4px 10px rgba(0,0,0,0.15);">', unsafe_allow_html=True)
                st.warning(f"{len(large_transactions)} potentially suspicious transactions (over ₹50,000)")
                
                # Display suspicious transactions
                display_sus = large_transactions[["user_name", "account_number", "type", "amount_formatted", "description", "date"]].rename(
                    columns={
                        "user_name": "name",
                        "account_number": "account",
                        "type": "type",
                        "amount_formatted": "amount",
                        "description": "description",
                        "date": "date"
                    }
                )
                st.dataframe(
                    display_sus,
                    height=300,
                    use_container_width=True,
                    hide_index=True
                )
                st.markdown('</div>', unsafe_allow_html=True)

def show_contact_messages():
    st.subheader("Contact Form Messages")
    
    # Custom CSS for contact messages section
    st.markdown("""
    <style>
    .message-card {
        background-color: #1E1E1E;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
        border-left: 4px solid #4F4FD3;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    .message-header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 10px;
        border-bottom: 1px solid #333;
        padding-bottom: 10px;
    }
    .sender-info {
        font-weight: bold;
    }
    .message-subject {
        color: #4F4FD3;
        margin-bottom: 10px;
        font-weight: 600;
    }
    .message-content {
        background-color: #262730;
        padding: 15px;
        border-radius: 6px;
        margin-bottom: 10px;
    }
    .message-meta {
        color: #999;
        font-size: 0.9em;
        text-align: right;
    }
    .message-actions {
        display: flex;
        justify-content: flex-end;
        gap: 10px;
        margin-top: 10px;
    }
    .filter-container {
        background-color: #262730;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Load contact messages from JSON file
    contact_messages = load_json_data(CONTACT_MESSAGES_FILE)
    
    if not contact_messages or "messages" not in contact_messages or not contact_messages["messages"]:
        st.info("No contact messages found.")
        return
    
    messages_list = contact_messages["messages"]
    
    # Convert to DataFrame for easier filtering and display
    df = pd.DataFrame(messages_list)
    
    # Sort by timestamp (newest first)
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp", ascending=False)
    
    # Display filters in a container
    with st.container():
        st.markdown('<div class="filter-container">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            # Filter by subject
            if "subject" in df.columns:
                unique_subjects = sorted(df["subject"].unique())
                selected_subject = st.selectbox("Filter by Subject", 
                                                options=["All"] + list(unique_subjects),
                                                index=0)
            
        with col2:
            # Date range filter
            if "timestamp" in df.columns:
                min_date = df["timestamp"].min().date()
                max_date = df["timestamp"].max().date()
                
                date_range = st.date_input("Date Range",
                                          value=(min_date, max_date),
                                          min_value=min_date,
                                          max_value=max_date)
                
                if len(date_range) == 2:
                    start_date, end_date = date_range
                else:
                    start_date, end_date = min_date, max_date
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Apply filters
    filtered_df = df.copy()
    
    if "subject" in df.columns and selected_subject != "All":
        filtered_df = filtered_df[filtered_df["subject"] == selected_subject]
    
    if "timestamp" in df.columns and len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df["timestamp"].dt.date >= start_date) & 
            (filtered_df["timestamp"].dt.date <= end_date)
        ]
    
    # Display message count
    st.write(f"Displaying {len(filtered_df)} of {len(df)} messages")
    
    # Display messages as cards
    for _, message in filtered_df.iterrows():
        st.markdown('<div class="message-card">', unsafe_allow_html=True)
        
        # Message header with sender info and timestamp
        st.markdown(f"""
        <div class="message-header">
            <div class="sender-info">{message.get('full_name', 'Unknown')}</div>
            <div>{message.get('timestamp', '')}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Contact details
        st.markdown(f"""
        <div>
            <strong>Email:</strong> {message.get('email', 'N/A')} | 
            <strong>Phone:</strong> {message.get('phone', 'N/A')}
        </div>
        """, unsafe_allow_html=True)
        
        # Subject and message content
        st.markdown(f'<div class="message-subject">{message.get("subject", "No Subject")}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="message-content">{message.get("message", "")}</div>', unsafe_allow_html=True)
        
        # Message actions
        st.markdown('<div class="message-actions">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 8])
        
        with col1:
            if st.button("Reply", key=f"reply_{_}"):
                # Open email client with pre-filled recipient
                import webbrowser
                webbrowser.open(f"mailto:{message.get('email', '')}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Call the main function to display the page based on login status
show_admin_page()
