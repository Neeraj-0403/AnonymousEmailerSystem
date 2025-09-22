# infrastructure/encryption_service.py

import os
from cryptography.fernet import Fernet
from infrastructure.logger import logger

class EncryptionService:
    """
    Handles the encryption and decryption of email content.
    """
    def __init__(self, key_path: str = "secret.key"):
        """
        Initializes the service by loading the encryption key.
        The key is required for both encryption and decryption.
        
        Args:
            key_path (str): The file path where the encryption key is stored.
        """
        self.key = self._load_key(key_path)
        self.fernet = Fernet(self.key)

    def _load_key(self, key_path: str) -> bytes:
        """Loads the encryption key from a file."""
        try:
            with open(key_path, "rb") as key_file:
                key = key_file.read()
                logger.info("Encryption key loaded successfully.")
                return key
        except FileNotFoundError:
            logger.error(f"Encryption key file not found at '{key_path}'. Please run the key generation script.")
            raise
        except Exception as e:
            logger.error(f"An error occurred while loading the encryption key: {e}")
            raise

    def encrypt(self, data: str) -> bytes:
        """Encrypts a string of data."""
        try:
            encrypted_data = self.fernet.encrypt(data.encode())
            logger.info("Data encrypted.")
            return encrypted_data
        except Exception as e:
            logger.error(f"Failed to encrypt data: {e}")
            raise

    def decrypt(self, encrypted_data: bytes) -> str:
        """Decrypts a byte string."""
        try:
            decrypted_data = self.fernet.decrypt(encrypted_data)
            logger.info("Data decrypted.")
            return decrypted_data.decode()
        except Exception as e:
            logger.error(f"Failed to decrypt data: {e}")
            raise
