# presentation/main.py

import sys
import os
import streamlit as st

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from application.auth_service import AuthService
from application.email_service import EmailService
from infrastructure.excel_repository import ExcelRepository
from infrastructure.ai_service import AIService
from infrastructure.encryption_service import EncryptionService
from infrastructure.logger import setup_logger, logger

# --- Initialization ---
# This part runs only once per app session
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.authenticated = False
    
    # Initialize infrastructure and application services
    try:
        encryption_service = EncryptionService()
        st.session_state.ai_service = AIService()
        st.session_state.excel_repository = ExcelRepository(auth_file='auth_codes.xlsx', email_file='emails_to_send.xlsx', encryption_service=encryption_service)
        st.session_state.auth_service = AuthService(auth_repository=st.session_state.excel_repository)
        st.session_state.email_service = EmailService(email_repository=st.session_state.excel_repository, ai_service=st.session_state.ai_service)
    except Exception as e:
        st.error(f"Failed to initialize the application. Please ensure `secret.key` and Excel files exist. Error: {e}")
        st.stop()

# --- Streamlit UI Components ---
st.set_page_config(page_title="Anonymous Email Sender", layout="centered")

# Simplify the background and use a known valid image URL
st.markdown(
    """
    <style>
        body {
            background-image: url('https://upload.wikimedia.org/wikipedia/commons/3/3c/Diwali_lights.jpg'); /* Known valid URL */
            background-color: #1a1a1a; /* Fallback color */
            background-size: cover;
            background-attachment: fixed;
        }

        .stButton button {
            background-color: #ff5722;
            color: white;
            font-size: 18px;
            border-radius: 10px;
        }

        .stTextInput input, .stTextArea textarea {
            border: 2px solid #ff9800;
            border-radius: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📮 Anonymous AI-Powered Email Sender")

# Add a simple description
st.markdown("""
Welcome to the Anonymous Email Sender. To use the system, you must first authenticate with a one-time access code. After sending an email, you will be required to enter a new code.
""")

# Add a festive animation banner
st.markdown("""
    <div style="text-align: center;">
        <h1 style="color: #ffcc00; animation: textGlow 2s infinite alternate;">🎆 Happy Diwali! 🎆</h1>
        <p style="font-size: 20px; color: #ffffff;">Enjoy the festival of lights with our Anonymous Email Sender!</p>
    </div>

    <style>
        @keyframes textGlow {
            0% { text-shadow: 0 0 10px #ffcc00; }
            100% { text-shadow: 0 0 20px #ffcc00; }
        }
    </style>
""", unsafe_allow_html=True)

if not st.session_state.authenticated:
    # Authentication form
    with st.form(key='auth_form'):
        st.subheader("Enter Your Access Code")
        auth_code = st.text_input("One-Time Code", placeholder="e.g., ABC-123").strip()
        submit_button = st.form_submit_button("Authenticate")

        if submit_button:
            if st.session_state.auth_service.validate_and_use_code(auth_code):
                st.session_state.authenticated = True
                st.success("Authentication successful! You can now send an email.")
                st.rerun()
            else:
                st.error("Invalid or already used code. Please try again.")

else:
    # Email submission form
    with st.form(key='email_form'):
        st.subheader("Compose Your Email")
        recipient = st.text_input("Recipient's Email", placeholder="john.doe@example.com").strip()
        subject = st.text_input("Subject").strip()
        content = st.text_area("Message Content", height=200).strip()
        submit_button = st.form_submit_button("Send Email")

        if submit_button:
            if not recipient or not subject or not content:
                st.warning("Please fill in all fields.")
            else:
                try:
                    is_queued = st.session_state.email_service.queue_email_for_sending(recipient, subject, content)
                    if is_queued:
                        st.success("Your email has been successfully queued! It will be sent by the background job shortly.")
                        # Reset the UI to the authentication screen after submission
                        st.session_state.authenticated = False
                        st.rerun()
                    else:
                        st.error("Failed to queue email. It may contain abusive content. Please revise and try again.")
                except Exception as e:
                    st.error(f"An error occurred while queuing the email: {e}")

# Footer or additional info
st.markdown("---")
st.markdown("The background job (`jobs/sender_job.py`) must be running to process queued emails.")
