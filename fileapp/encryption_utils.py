import base64
from cryptography.fernet import Fernet
from django.conf import settings

def load_key():
    return settings.SECRET_KEY[:32].encode('utf-8').ljust(32, b'0')

def encrypt_file(file_data: bytes) -> bytes:
    fernet = Fernet(base64.urlsafe_b64encode(load_key()))
    return fernet.encrypt(file_data)

def decrypt_file(encrypted_data: bytes) -> bytes:
    fernet = Fernet(base64.urlsafe_b64encode(load_key()))
    return fernet.decrypt(encrypted_data)
