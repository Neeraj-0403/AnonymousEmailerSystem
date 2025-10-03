# infrastructure/encryption_service.py

import base64
from cryptography.fernet import Fernet
from infrastructure.logger import logger
from dotenv import load_dotenv
import os

load_dotenv()
class EncryptionService:
    """
    Handles the encryption and decryption of email content.
    """
    def __init__(self):
        """
        Initializes the service by loading the encryption key.
        The key is required for both encryption and decryption.
        
        Args:
            key_path (str): The file path where the encryption key is stored.
        """
        self.key = self._load_key()
        self.fernet = Fernet(self.key)

    def _load_key(self) -> bytes:
        """Loads the encryption key from a file."""
        try: 
            key = os.getenv('SECRET_KEY')
            logger.info("Encryption key loaded successfully.")
            return key
        except FileNotFoundError:
             raise
        except Exception as e:
            logger.error(f"An error occurred while loading the encryption key: {e}")
            raise

    def encrypt(self, data: str) -> str:
        """Encrypts a string of data and returns base64 encoded string for CSV storage."""
        try:
            encrypted_data = self.fernet.encrypt(data.encode())
            # Convert to base64 string for CSV storage
            encrypted_string = base64.b64encode(encrypted_data).decode('utf-8')
            logger.info("Data encrypted.")
            return encrypted_string
        except Exception as e:
            logger.error(f"Failed to encrypt data: {e}")
            raise

    def decrypt(self, encrypted_data: str) -> str:
        """Decrypts encrypted data from CSV storage."""
        try:
            # Handle string representation of bytes (e.g., "b'...")
            if isinstance(encrypted_data, str) and encrypted_data.startswith("b'") and encrypted_data.endswith("'"):
                # Remove b' and ' wrapper - this is the Fernet token itself
                fernet_token = encrypted_data[2:-1]
                # Fernet token is already properly encoded, use directly as bytes
                encrypted_bytes = fernet_token.encode('utf-8')
            elif isinstance(encrypted_data, bytes):
                encrypted_bytes = encrypted_data
            else:
                # Direct string to bytes for Fernet token
                encrypted_bytes = encrypted_data.encode('utf-8')
            
            decrypted_data = self.fernet.decrypt(encrypted_bytes)
            logger.info("Data decrypted successfully.")
            return decrypted_data.decode()
        except Exception as e:
            logger.error(f"Failed to decrypt data: {e}")
            raise
