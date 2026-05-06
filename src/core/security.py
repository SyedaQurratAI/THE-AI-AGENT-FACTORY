import os
from cryptography.fernet import Fernet
from src.core.config import settings
from src.utils.logger import logger

class SecurityManager:
    """Manages encryption and decryption of sensitive data using Fernet."""
    def __init__(self):
        """Initializes the manager and loads or creates the encryption key."""
        self.key_path = os.path.join(settings.DATA_DIR, ".secret.key")
        self.key = self._get_or_create_key()
        self.fernet = Fernet(self.key)

    def _get_or_create_key(self) -> bytes:
        """Retrieves an existing key or generates a new one."""
        if os.path.exists(self.key_path):
            with open(self.key_path, "rb") as f:
                return f.read()
        
        logger.info("Generating new encryption key...")
        key = Fernet.generate_key()
        os.makedirs(os.path.dirname(self.key_path), exist_ok=True)
        with open(self.key_path, "wb") as f:
            f.write(key)
        return key

    def encrypt(self, data: str) -> str:
        """Encrypts a string and returns the ciphertext."""
        return self.fernet.encrypt(data.encode()).decode()

    def decrypt(self, token: str) -> str:
        """Decrypts a ciphertext and returns the original string."""
        return self.fernet.decrypt(token.encode()).decode()

security_manager = SecurityManager()
