# generate_key.py

from cryptography.fernet import Fernet
import os

try:
    # Generate a new key.
    key = Fernet.generate_key()

    # Save the key to a file.
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    
    print("Encryption key 'secret.key' generated successfully in the project root.")
    print("This key is required to encrypt and decrypt email content.")

except ImportError:
    print("Error: 'cryptography' library not found.")
    print("Please install it by running: pip install cryptography")
except Exception as e:
    print(f"An error occurred while generating the key: {e}")
