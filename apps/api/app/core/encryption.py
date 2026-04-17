from cryptography.fernet import Fernet

from app.core.config import settings


class CodeEncryptionService:
    def __init__(self) -> None:
        self.fernet = Fernet(settings.encryption_key.encode())

    def encrypt(self, value: str) -> str:
        return self.fernet.encrypt(value.encode()).decode()

    def decrypt(self, value: str) -> str:
        return self.fernet.decrypt(value.encode()).decode()


code_encryption = CodeEncryptionService()
