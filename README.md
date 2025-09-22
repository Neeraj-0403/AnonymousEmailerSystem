Anonymous AI-Powered Email Sender
This project implements a simple, anonymous email sender system based on a clean architecture. It uses a one-time code system for access and an AI-like content filter to prevent abusive emails. The system is designed to queue emails and send them asynchronously via a separate job.

Features
Clean Architecture: The codebase is organized into domain, application, infrastructure, and presentation layers for modularity and maintainability.

One-Time Access Codes: Users must enter a valid, one-time-use code to access the email sending functionality. These codes are managed in an Excel file.

AI Content Moderation: A simple AI-like check is implemented to flag and prevent the sending of potentially abusive content.

Encrypted Content: The email content is encrypted before being stored, ensuring privacy.

Asynchronous Email Sending: Emails are not sent immediately. They are queued in an Excel file and processed in batches by a separate job script.

Comprehensive Logging: The system logs activities, errors, and email sending status to a dedicated log file.

Simple UI: The command-line interface has been replaced with a simple and attractive web UI built with Streamlit.

Folder Structure
├── application/
│ ├── auth_service.py
│ └── email_service.py
├── domain/
│ ├── models.py
│ ├── auth_repository.py
│ └── email_repository.py
├── infrastructure/
│ ├── ai_service.py
│ ├── excel_repository.py
│ ├── encryption_service.py
│ └── email_sender.py
├── jobs/
│ └── sender_job.py
├── presentation/
│ └── main.py
├── requirements.txt
├── auth_codes.xlsx
├── emails_to_send.xlsx
└── run.bat (or run.sh)

Setup
Clone the repository:

git clone <repository_url>
cd anonymous-email-sender

Create a virtual environment (recommended):

python -m venv venv

# On Windows

venv\Scripts\activate

# On macOS/Linux

source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Prepare Excel Files:

auth_codes.xlsx: Create an Excel file named auth_codes.xlsx with a single sheet and two columns: code and is_used. Populate the code column with unique, one-time access codes (e.g., XYZ123). The is_used column should initially be FALSE for all codes.

emails_to_send.xlsx: Create an empty Excel file named emails_to_send.xlsx with the following columns: id, recipient, subject, encrypted_content, is_sent, and sent_timestamp. The system will automatically add data to this file.

Generate an Encryption Key:

The system uses a secret key to encrypt email content. Run the following command once to generate a key and save it to a file named secret.key.

python -c "from cryptography.fernet import Fernet; key = Fernet.generate_key(); with open('secret.key', 'wb') as key_file: key_file.write(key)"

Run the application:

To use the web UI, run main.py using Streamlit:

streamlit run presentation/main.py

To run the background job that sends the queued emails, run sender_job.py:

python jobs/sender_job.py

How It Works
Authentication: The Streamlit app starts by showing an authentication form for a one-time access code.

It reads auth_codes.xlsx.

If the entered code is found and its is_used status is FALSE, the user is authenticated, and the UI transitions to the email submission form.

The is_used status for that code is immediately updated to TRUE in the Excel file.

Email Submission:

After authentication, the user can input the email recipient, subject, and content into the web form.

The AIService checks the content for abusive keywords.

The EncryptionService encrypts the email content.

The ExcelRepository saves the email record to emails_to_send.xlsx with is_sent as FALSE.

The Job (sender_job.py):

This script should be run periodically (e.g., every minute via a cron job or Windows Task Scheduler).

It reads emails_to_send.xlsx.

It identifies and processes up to 10 emails with is_sent as FALSE.

For each email, it decrypts the content and sends it via the EmailSender.

After successful sending, it updates the is_sent status to TRUE and adds a timestamp.

Looping: After each successful email submission, the Streamlit UI automatically resets and returns to the authentication screen, requiring a new code for the next email.
