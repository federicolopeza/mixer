import json
import os

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

SALT_SIZE = 16
NONCE_SIZE = 16
TAG_SIZE = 16
KEY_SIZE = 32


def encrypt_data(data: dict, password: str) -> bytes:
    """Encripta un diccionario usando AES-256-GCM con una contraseña."""
    salt = os.urandom(SALT_SIZE)
    # Derivar clave con PBKDF2-HMAC-SHA256
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=1000000,
        backend=default_backend(),
    )
    key = kdf.derive(password.encode("utf-8"))
    aesgcm = AESGCM(key)
    nonce = os.urandom(NONCE_SIZE)
    plaintext = json.dumps(data, indent=4).encode("utf-8")
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    return salt + nonce + ciphertext


def decrypt_data(encrypted_data: bytes, password: str) -> dict:
    """Desencripta datos encriptados con AES-256-GCM."""
    try:
        salt = encrypted_data[:SALT_SIZE]
        nonce = encrypted_data[SALT_SIZE : SALT_SIZE + NONCE_SIZE]
        ciphertext = encrypted_data[SALT_SIZE + NONCE_SIZE :]
        # Derivar clave con PBKDF2-HMAC-SHA256
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=KEY_SIZE,
            salt=salt,
            iterations=1000000,
            backend=default_backend(),
        )
        key = kdf.derive(password.encode("utf-8"))
        aesgcm = AESGCM(key)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        return json.loads(plaintext.decode("utf-8"))
    except (ValueError, KeyError, InvalidTag) as e:
        raise ValueError(
            "Error de desencriptación. Contraseña incorrecta o datos corruptos."
        ) from e
