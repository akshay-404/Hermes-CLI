import secrets
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ed25519, x25519
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from dataclasses import dataclass


@dataclass
class SenderKeyPackage:
    sender: str
    recipient: str
    room_id: str
    key_id: str
    nonce: bytes
    ciphertext: bytes
    signature: bytes


def derive_distribution_key(shared_secret: bytes) -> bytes:
    return HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"Hermes Sender Key Distribution v1",
    ).derive(shared_secret)


def encrypt_sender_key(sender_key: bytes, encryption_key: bytes) -> tuple[bytes, bytes]:
    nonce = secrets.token_bytes(12)
    cipher = ChaCha20Poly1305(encryption_key)
    ciphertext = cipher.encrypt(nonce, sender_key, None)
    return nonce, ciphertext


def decrypt_sender_key(ciphertext: bytes, nonce: bytes, encryption_key: bytes) -> bytes:
    cipher = ChaCha20Poly1305(encryption_key)
    return cipher.decrypt(nonce, ciphertext, None)


def sign_sender_key_package(signing_private_key: ed25519.Ed25519PrivateKey, ciphertext: bytes, nonce: bytes) -> bytes:
    data = nonce + ciphertext
    return signing_private_key.sign(data)


def verify_sender_key_package(signing_public_key: ed25519.Ed25519PublicKey, ciphertext: bytes, nonce: bytes, signature: bytes) -> bool:
    data = nonce + ciphertext
    try:
        signing_public_key.verify(signature, data)
        return True
    except Exception:
        return False


def create_sender_key_package(
    sender: str,
    recipient: str,
    room_id: str,
    key_id: str,
    sender_key: bytes,
    sender_signing_private: ed25519.Ed25519PrivateKey,
    sender_exchange_private: x25519.X25519PrivateKey,
    recipient_exchange_public: x25519.X25519PublicKey,
) -> SenderKeyPackage:

    shared_secret = sender_exchange_private.exchange(recipient_exchange_public)
    encryption_key = derive_distribution_key(shared_secret)
    nonce, ciphertext = encrypt_sender_key(
        sender_key,
        encryption_key,
    )
    signature = sign_sender_key_package(
        sender_signing_private,
        ciphertext,
        nonce,
    )
    return SenderKeyPackage(
        sender=sender,
        recipient=recipient,
        room_id=room_id,
        key_id=key_id,
        nonce=nonce,
        ciphertext=ciphertext,
        signature=signature,
    )


def open_sender_key_package(
    package: SenderKeyPackage,
    recipient_exchange_private: x25519.X25519PrivateKey,
    sender_exchange_public: x25519.X25519PublicKey,
    sender_signing_public: ed25519.Ed25519PublicKey,
) -> bytes:

    valid = verify_sender_key_package(
        sender_signing_public,
        package.ciphertext,
        package.nonce,
        package.signature,
    )
    if not valid:
        raise ValueError(
            "Invalid sender-key package signature"
        )

    shared_secret = recipient_exchange_private.exchange(sender_exchange_public)
    encryption_key = derive_distribution_key(shared_secret)

    return decrypt_sender_key(
        package.ciphertext,
        package.nonce,
        encryption_key,
    )
