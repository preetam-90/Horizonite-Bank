import streamlit as st
import webbrowser
import json
import os
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Contact Us - Horizonite Bank", layout="wide")

# Custom CSS with improved color palette
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #073590 0%, #2563EB 100%);
        color: white;
        padding: 2.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(37, 99, 235, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-header h1 {
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 0.8rem;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.95;
        max-width: 800px;
        margin: 0 auto;
    }
    
    .contact-card {
        background: linear-gradient(145deg, #182338 0%, #1F2A40 100%);
        border-radius: 16px;
        padding: 1.8rem;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        height: 100%;
        transition: transform 0.3s, box-shadow 0.3s;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    .contact-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.25);
    }
    
    .contact-card h3 {
        color: #4F95FF;
        font-weight: 600;
        margin-bottom: 1.2rem;
        border-bottom: 2px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 0.75rem;
    }
    
    .contact-method {
        display: flex;
        align-items: center;
        padding: 1rem 0;
        margin-bottom: 1rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.07);
        transition: background-color 0.2s;
        border-radius: 8px;
    }
    
    .contact-method:hover {
        background-color: rgba(79, 149, 255, 0.08);
    }
    
    .contact-method:last-child {
        border-bottom: none;
        margin-bottom: 0;
    }
    
    .contact-icon {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin-right: 1.2rem;
        flex-shrink: 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    .contact-icon.email {
        background: linear-gradient(135deg, #F43F5E 0%, #FB7185 100%);
        color: #FFFFFF;
    }
    
    .contact-icon.phone {
        background: linear-gradient(135deg, #10B981 0%, #34D399 100%);
        color: #FFFFFF;
    }
    
    .contact-icon.whatsapp {
        background: linear-gradient(135deg, #25D366 0%, #4ADE80 100%);
        color: #FFFFFF;
    }
    
    .contact-icon.linkedin {
        background: linear-gradient(135deg, #0E76A8 0%, #38BDF8 100%);
        color: #FFFFFF;
    }
    
    .contact-icon.location {
        background: linear-gradient(135deg, #F59E0B 0%, #FBBF24 100%);
        color: #FFFFFF;
    }

    .contact-content {
        flex-grow: 1;
    }
    
    .contact-content h4 {
        margin: 0 0 0.2rem 0;
        color: #FFFFFF;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    .contact-content p {
        color: rgba(255, 255, 255, 0.85);
        margin: 0 0 0.25rem 0;
        font-size: 0.9rem;
    }
    
    .contact-action {
        background: rgba(79, 149, 255, 0.15);
        color: #FFFFFF;
        border: 1px solid rgba(79, 149, 255, 0.4);
        border-radius: 10px;
        padding: 0.7rem 1.2rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
        text-decoration: none;
        display: inline-block;
        text-align: center;
        font-size: 0.95rem;
        white-space: nowrap;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
    }
    
    .contact-action:hover {
        background: rgba(79, 149, 255, 0.25);
        color: #FFFFFF;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
        transform: translateY(-2px);
    }
    
    .contact-action.email {
        background: rgba(244, 63, 94, 0.15);
        border: 1px solid rgba(244, 63, 94, 0.4);
    }
    
    .contact-action.email:hover {
        background: rgba(244, 63, 94, 0.25);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
    }
    
    .contact-action.phone {
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.4);
    }
    
    .contact-action.phone:hover {
        background: rgba(16, 185, 129, 0.25);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
    }
    
    .contact-action.whatsapp {
        background: rgba(37, 211, 102, 0.15);
        border: 1px solid rgba(37, 211, 102, 0.4);
    }
    
    .contact-action.whatsapp:hover {
        background: rgba(37, 211, 102, 0.25);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
    }
    
    .contact-action.linkedin {
        background: rgba(14, 118, 168, 0.15);
        border: 1px solid rgba(14, 118, 168, 0.4);
    }
    
    .contact-action.linkedin:hover {
        background: rgba(14, 118, 168, 0.25);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
    }
    
    .map-container {
        border-radius: 16px;
        overflow: hidden;
        height: 400px;
        width: 100%;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        margin: 1rem auto;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    .contact-form label {
        font-weight: 500;
        color: #F0F4F8;
    }
    
    .form-submit-button {
        background: linear-gradient(135deg, #2563EB 0%, #4F95FF 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
        width: 100%;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    }
    
    .form-submit-button:hover {
        background: linear-gradient(135deg, #1E40AF 0%, #2563EB 100%);
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.4);
        transform: translateY(-2px);
    }

    .contact-info-wrapper {
        display: flex;
        flex-direction: column;
    }

    .map-and-contact {
        display: flex;
        flex-direction: column;
    }

    @media (min-width: 992px) {
        .map-and-contact {
            flex-direction: row;
            align-items: flex-start;
            gap: 1.5rem;
        }
        
        .contact-info-wrapper {
            flex: 3;
        }
        
        .map-wrapper {
            flex: 2;
            position: sticky;
            top: 1rem;
        }
    }

    /* Remove default Streamlit padding */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }

    /* Hide empty elements */
    .st-emotion-cache-e3xfei {
        margin-top: 0 !important;
    }

    /* Remove extra whitespace around containers */
    .st-emotion-cache-z5fcl4 {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }

    /* Reset margin for all streamlit elements */
    .element-container {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }
    
    div[data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }
    
    /* Fix icon display issues */
    .contact-icon i {
        font-size: 1.5rem;
    }
    
    /* Ensure proper spacing in contact method */
    .contact-method {
        position: relative;
        padding: 1rem 0.8rem;
    }
    
    /* Fix action button positioning */
    .contact-action {
        position: relative;
        display: inline-block;
        margin-left: auto;
    }
    
    /* Ensure proper contact method layout */
    .contact-method {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: nowrap;
    }
    
    /* Business hours table styling for dark mode */
    table {
        width: 100%;
    }
    
    table strong {
        color: #FFFFFF;
    }
    
    table td {
        color: rgba(255, 255, 255, 0.85);
    }
    
    /* Improve visibility for form inputs and labels */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea, 
    .stSelectbox > div > div > div {
        border-color: rgba(79, 149, 255, 0.3) !important;
        color: #FFFFFF !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px !important;
    }
    
    .stTextInput > div > div > input:focus, 
    .stTextArea > div > div > textarea:focus, 
    .stSelectbox > div > div > div:focus {
        border-color: rgba(79, 149, 255, 0.7) !important;
        box-shadow: 0 0 0 1px rgba(79, 149, 255, 0.3) !important;
    }
    
    .stCheckbox > div > label {
        color: #FFFFFF !important;
    }
    
    /* Add subtle gradient backgrounds to make text more readable */
    .contact-method {
        background: linear-gradient(90deg, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0) 100%);
        border-bottom: 1px solid rgba(255, 255, 255, 0.07);
    }
    
    .contact-method:hover {
        background: linear-gradient(90deg, rgba(255,255,255,0.07) 0%, rgba(255,255,255,0.02) 100%);
    }
    
    /* Custom scrollbar for the page */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0F172A;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #475569;
    }
</style>
""", unsafe_allow_html=True)

# Developer Information Section
st.markdown('<div style="margin-top: 3rem; text-align: center;">', unsafe_allow_html=True)
st.markdown('<h3 style="color: #FFFFFF; margin-bottom: 1rem;">Developer Information</h3>', unsafe_allow_html=True)
st.markdown("""
<div style="background: linear-gradient(135deg, rgba(30, 58, 138, 0.7) 0%, rgba(37, 99, 235, 0.7) 100%); border-radius: 12px; padding: 25px; max-width: 650px; margin: 0 auto; box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3); border: 1px solid rgba(255, 255, 255, 0.1);">
    <div style="display: flex; justify-content: center; margin-bottom: 15px;">
        <div style="background-color: rgba(255, 255, 255, 0.1); width: 80px; height: 80px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
            <i class="fas fa-code" style="font-size: 30px; color: #FFFFFF;"></i>
        </div>
    </div>
    <p style="color: #FFFFFF; font-size: 18px; margin-bottom: 8px; font-weight: 600;">Developed by: Preetam Kumar</p>
    <p style="color: #FFFFFF; font-size: 16px; margin-bottom: 8px;"><strong>College:</strong> Meerut Institute of Technology</p>
    <p style="color: #FFFFFF; font-size: 16px; margin-bottom: 8px;"><strong>Program:</strong> B.Tech 7th Semester</p>
    <p style="color: #FFFFFF; font-size: 16px; margin-bottom: 8px;"><strong>Registration Number:</strong> U19KU22S0084</p>
    <p style="color: #FFFFFF; font-size: 16px; margin-bottom: 15px;"><strong>Project:</strong> Horizonite Bank Portal</p>
    <div style="height: 1px; background: linear-gradient(to right, transparent, rgba(255, 255, 255, 0.3), transparent); margin: 15px 0;"></div>
  
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Function to handle redirects
def open_email():
    webbrowser.open('mailto:preetamkumar8873@gmail.com')

def open_phone():
    webbrowser.open('tel:+919798292134')

def open_whatsapp():
    # Using the WhatsApp API to open chat with the bank's number
    webbrowser.open('https://wa.me/9798292134')

def open_linkedin():
    webbrowser.open('https://www.linkedin.com/in/preetam-90')

# Header section
st.markdown("""
<div class="main-header">
    <h1>Contact Horizonite Bank</h1>
    <p>We're here to help you with any questions or concerns. Reach out to us through your preferred communication channel.</p>
</div>
""", unsafe_allow_html=True)

# Main content columns - directly creating columns without extra containers
left_col, right_col = st.columns([3, 2], gap="small")

with left_col:
    # Contact info wrapper - no extra divs
    with st.container():
        # Contact methods card
        st.markdown('<div class="contact-card">', unsafe_allow_html=True)
        st.markdown('<h3>Get in Touch</h3>', unsafe_allow_html=True)
        
        # Email contact method
        st.markdown("""
        <div class="contact-method">
            <div class="contact-icon email">
                <i class="fas fa-envelope"></i>
            </div>
            <div class="contact-content">
                <h4>Email Us</h4>
                <p>For general inquiries and support requests</p>
                <p>preetamkumar8873@gmail.com</p>
            </div>
            <a href="mailto:preetamkumar8873@gmail.com" class="contact-action email">
                Send Email
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        # Phone contact method
        st.markdown("""
        <div class="contact-method">
            <div class="contact-icon phone">
                <i class="fas fa-phone-alt"></i>
            </div>
            <div class="contact-content">
                <h4>Call Us</h4>
                <p>Customer Service Hotline</p>
                <p>+91 9798292134</p>
            </div>
            <a href="tel:+919798292134" class="contact-action phone">
                Call Now
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        # WhatsApp contact method
        st.markdown("""
        <div class="contact-method">
            <div class="contact-icon whatsapp">
                <i class="fab fa-whatsapp"></i>
            </div>
            <div class="contact-content">
                <h4>WhatsApp</h4>
                <p>Chat with our customer support team</p>
                <p>+91 8539038946</p>
            </div>
            <a href="https://wa.me/918539038946" class="contact-action whatsapp">
                Chat Now
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        # LinkedIn contact method
        st.markdown("""
        <div class="contact-method">
            <div class="contact-icon linkedin">
                <i class="fab fa-linkedin-in"></i>
            </div>
            <div class="contact-content">
                <h4>Connect on LinkedIn</h4>
                <p>Follow us for updates and career opportunities</p>
                <p>Preetam kumar</p>
            </div>
            <a href="https://www.linkedin.com/in/preetam-90" target="_blank" class="contact-action linkedin">
                Connect
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        # Office location method
        st.markdown("""
        <div class="contact-method">
            <div class="contact-icon location">
                <i class="fas fa-map-marker-alt"></i>
            </div>
            <div class="contact-content">
                <h4>Head Office</h4>
                <p>Esteem Embelem</p>
                <p>Electronic City,Bengaluru, 560100, India</p>
            </div>
            <a href="https://maps.google.com/?q=Electronic+City,+Bengaluru,+560100,+India" target="_blank" class="contact-action" style="background-color: #475569; border: 1px solid #64748B;">
                Get Directions
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Map container - directly adding without wrappers
    st.markdown('<div class="map-container">', unsafe_allow_html=True)
    st.markdown("""
    <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3889.6495832336394!2d77.68251477415968!3d12.838014686705725!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3bae6cf6518eb24f%3A0x958a90b8dbde166a!2sEsteem%20Emblem!5e0!3m2!1sen!2sin!4v1714490245592!5m2!1sen!2sin" 
    width="100%" height="100%" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right_col:
    # Contact form card - direct container
    st.markdown('<div class="contact-card">', unsafe_allow_html=True)
    st.markdown('<h3>Send Us a Message</h3>', unsafe_allow_html=True)
    
    with st.form("contact_form", clear_on_submit=True):
        full_name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        
        subject = st.selectbox("Subject", [
            "General Inquiry", 
            "Account Services", 
            "Loan Information", 
            "Investment Advice",
            "Mobile Banking Support",
            "Report an Issue",
            "Other"
        ])
        
        message = st.text_area("Your Message", height=120)
        
        # Terms agreement
        terms = st.checkbox("I agree to the privacy policy and terms of service")
        
        submit = st.form_submit_button("Submit Message", use_container_width=True)
        
        if submit:
            if not all([full_name, email, message]):
                st.error("Please fill in all required fields.")
            elif not terms:
                st.error("Please agree to our privacy policy and terms of service.")
            else:
                # Save the contact form data to a JSON file
                contact_data = {
                    "full_name": full_name,
                    "email": email,
                    "phone": phone,
                    "subject": subject,
                    "message": message,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # Define the path for the JSON file
                json_file_path = "data/contact_messages.json"
                
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
                
                # Check if file exists and load existing data
                if os.path.exists(json_file_path):
                    with open(json_file_path, "r") as f:
                        try:
                            all_contacts = json.load(f)
                        except json.JSONDecodeError:
                            # If the file is empty or has invalid JSON
                            all_contacts = {"messages": []}
                else:
                    all_contacts = {"messages": []}
                
                # Add new message to the list
                all_contacts["messages"].append(contact_data)
                
                # Save the updated data back to the file
                with open(json_file_path, "w") as f:
                    json.dump(all_contacts, f, indent=4)
                
                st.success("Thank you for your message! Our team will get back to you shortly.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Business hours card - direct container
    st.markdown('<div class="contact-card">', unsafe_allow_html=True)
    st.markdown('<h3>Business Hours</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    <table style="width: 100%;">
        <tr>
            <td style="padding: 8px 0; border-bottom: 1px solid #f0f4f8;"><strong>Monday - Friday</strong></td>
            <td style="padding: 8px 0; border-bottom: 1px solid #f0f4f8;">9:00 AM - 5:00 PM</td>
        </tr>
        <tr>
            <td style="padding: 8px 0; border-bottom: 1px solid #f0f4f8;"><strong>Saturday</strong></td>
            <td style="padding: 8px 0; border-bottom: 1px solid #f0f4f8;">10:00 AM - 2:00 PM</td>
        </tr>
        <tr>
            <td style="padding: 8px 0;"><strong>Sunday</strong></td>
            <td style="padding: 8px 0;">Closed</td>
        </tr>
    </table>
    
    <div style="margin-top: 1rem;">
        <h4 style="color: #FFFFFF; font-size: 1.1rem;">Customer Service Availability</h4>
        <p style="color: #FFFFFF;">Our 24/7 phone support is available at +91 8539038946 for emergencies such as lost cards or suspicious transactions.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Add Font Awesome for icons
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
""", unsafe_allow_html=True)

# Buttons for direct contact actions - only visible on mobile
st.markdown("""
<div style="display: none; position: fixed; bottom: 20px; right: 20px; z-index: 1000;" class="mobile-contact-buttons">
    <a href="mailto:preetamkumar8873@gmail.com" style="background-color: #DB2777; color: white; padding: 12px; border-radius: 50%; display: inline-block; margin-right: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
        <i class="fas fa-envelope"></i>
    </a>
    <a href="tel:+919798292134" style="background-color: #10B981; color: white; padding: 12px; border-radius: 50%; display: inline-block; margin-right: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
        <i class="fas fa-phone-alt"></i>
    </a>
    <a href="https://wa.me/918539038946" style="background-color: #25D366; color: white; padding: 12px; border-radius: 50%; display: inline-block; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
        <i class="fab fa-whatsapp"></i>
    </a>
</div>

<style>
@media (max-width: 768px) {
    .mobile-contact-buttons {
        display: block !important;
    }
}
</style>
""", unsafe_allow_html=True)
