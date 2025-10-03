# Flask Backend
import sys
import os
from flask import Flask, render_template, request, jsonify
import pygame
import pyotp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from application.email_service import EmailService
from infrastructure.csv_repository import CSVRepository
from infrastructure.ai_service import AIService
from infrastructure.encryption_service import EncryptionService
from infrastructure.logger import setup_logger, logger

app = Flask(__name__)

# Initialize services
encryption_service = EncryptionService()
ai_service = AIService()
csv_repository = CSVRepository(
    email_file='data/emails_to_send.csv',
    encryption_service=encryption_service
)
email_service = EmailService(
    email_repository=csv_repository,
    ai_service=ai_service
)

# Initialize pygame for sound
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    try:
        data = request.get_json()
        auth_code = data.get('auth_code', '').strip()
        
        print(f"DEBUG: Received auth_code: '{auth_code}'")
        
        if not auth_code or len(auth_code) != 6:
            return jsonify({'success': False, 'message': 'Please enter a valid 6-digit MFA code.'})
        
        # Load TOTP secret
        with open('totp_secret.txt', 'r') as f:
            secret = f.read().strip()
        
        print(f"DEBUG: Using secret: {secret[:10]}...")
        
        # Validate TOTP code
        totp = pyotp.TOTP(secret)
        current_code = totp.now()
        print(f"DEBUG: Current valid code: {current_code}")
        
        if totp.verify(auth_code, valid_window=2):
            return jsonify({'success': True, 'message': 'Secret Authentication successful!'})
        else:
            return jsonify({'success': False, 'message': 'Invalid secret code. Please check your authenticator app and try again.'})
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        print(f"DEBUG: Exception: {e}")
        return jsonify({'success': False, 'message': f'Authentication failed: {str(e)}'})

@app.route('/get_contacts', methods=['GET'])
def get_contacts():
    try:
        import pandas as pd
        contacts_file = 'data/contacts.csv'
        
        if os.path.exists(contacts_file):
            df = pd.read_csv(contacts_file)
            contacts = []
            for _, row in df.iterrows():
                contacts.append({
                    'name': row.get('name', ''),
                    'email': row.get('email', '')
                })
            return jsonify(contacts)
        else:
            return jsonify([
                {'name': 'Alice Johnson', 'email': 'alice@example.com'},
                {'name': 'Bob Smith', 'email': 'bob@example.com'},
                {'name': 'Carol Davis', 'email': 'carol@example.com'}
            ])
    except Exception as e:
        return jsonify([{'name': 'Default User', 'email': 'user@example.com'}])

@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        data = request.get_json()
        recipient = data.get('recipient', '').strip()
        subject = data.get('subject', '').strip()
        content = data.get('content', '').strip()
        
        if not recipient or not subject or not content:
            return jsonify({'success': False, 'message': 'Please fill in all fields.'})
        
        # Check for inappropriate content FIRST
        if ai_service.check_for_abuse(content):
            return jsonify({
                'success': False, 
                'message': 'Your message contains inappropriate, abusive, or sexual content. Please modify your message to be respectful and appropriate.'
            })
        
        is_queued = email_service.queue_email_for_sending(recipient, subject, content)
        
        if is_queued:
            return jsonify({'success': True, 'message': 'Email queued successfully!'})
        else:
            return jsonify({'success': False, 'message': 'Failed to queue email. May contain inappropriate content.'})
    except Exception as e:
        logger.error(f"Email sending error: {e}")
        return jsonify({'success': False, 'message': 'An error occurred while queuing the email.'})

if __name__ == '__main__':
    # Create sample contacts file if it doesn't exist
    import pandas as pd
    
    contacts_file = 'data/contacts.csv'
    if not os.path.exists(contacts_file):
        sample_contacts = pd.DataFrame({
            'name': ['Alice Johnson', 'Bob Smith', 'Carol Davis', 'David Wilson', 'Emma Brown'],
            'email': ['alice@example.com', 'bob@example.com', 'carol@example.com', 'david@example.com', 'emma@example.com']
        })
        sample_contacts.to_csv(contacts_file, index=False)
    
    app.run(host='0.0.0.0', port=5000, debug=False)