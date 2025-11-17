import os
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

def generate_salt(size: int = 32) -> bytes:
    """Generate a cryptographically secure salt"""
    return os.urandom(size)

def derive_key(master_password: str, salt: bytes, iterations: int = 100000) -> bytes:
    """Derive a 256-bit key from master password using PBKDF2"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # 256-bit key for AES-256
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    return kdf.derive(master_password.encode('utf-8'))

def verify_key(master_password: str, salt: bytes, derived_key: bytes, iterations: int = 100000) -> bool:
    """Verify if master password produces the same derived key"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    try:
        kdf.verify(master_password.encode('utf-8'), derived_key)
        return True
    except Exception:
        return False