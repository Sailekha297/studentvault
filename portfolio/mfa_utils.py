
import base64
import hashlib

from cryptography.fernet import Fernet
from django.conf import settings


def get_fernet():
    key = hashlib.sha256(
        settings.SECRET_KEY.encode()
    ).digest()

    return Fernet(base64.urlsafe_b64encode(key))


def encrypt_secret(secret):
    return get_fernet().encrypt(
        secret.encode()
    ).decode()


def decrypt_secret(encrypted_secret):
    return get_fernet().decrypt(
        encrypted_secret.encode()
    ).decode()
