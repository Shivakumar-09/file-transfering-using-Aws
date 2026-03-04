import os
import io
from cryptography.fernet import Fernet
from config import Config

class EncryptionManager:
    """Uses AES-256 (via Fernet) to encrypt and decrypt files."""
    
    def __init__(self):
        # Fernet requires a base64 encoded 32-byte key
        self.key = Config.ENCRYPTION_KEY.encode()
        try:
            self.fernet = Fernet(self.key)
        except Exception as e:
            # Fallback/Generate if invalid (only for dev/testing)
            print(f"Encryption Init Error: {e}. Ensure ENCRYPTION_KEY is a valid 32-byte base64 string.")
            self.key = Fernet.generate_key()
            self.fernet = Fernet(self.key)

    def encrypt_file(self, file_data: bytes) -> bytes:
        """Encrypts raw bytes and returns encrypted bytes."""
        return self.fernet.encrypt(file_data)

    def decrypt_file(self, encrypted_data: bytes) -> bytes:
        """Decrypts encrypted bytes and returns raw bytes."""
        return self.fernet.decrypt(encrypted_data)

    def encrypt_stream(self, input_stream):
        """Encrypts a file-like stream and returns a BytesIO object."""
        raw_data = input_stream.read()
        encrypted_data = self.encrypt_file(raw_data)
        return io.BytesIO(encrypted_data)

    def decrypt_to_stream(self, encrypted_data: bytes):
        """Decrypts data and returns a BytesIO object."""
        decrypted_data = self.decrypt_file(encrypted_data)
        return io.BytesIO(decrypted_data)
