import secrets
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305


def encrypt_message(message_key: bytes, plaintext: bytes) -> tuple[bytes, bytes]:
    nonce = secrets.token_bytes(12)
    cipher = ChaCha20Poly1305(message_key)
    ciphertext = cipher.encrypt(
        nonce,
        plaintext,
        None,
    )
    return nonce, ciphertext


def decrypt_message(message_key: bytes, nonce: bytes, ciphertext: bytes) -> bytes:
    cipher = ChaCha20Poly1305(message_key)
    return cipher.decrypt(
        nonce,
        ciphertext,
        None,
    )
