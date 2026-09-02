import base64
import secrets
from cryptography.hazmat.primitives.asymmetric import ed25519, x25519
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

def generate_identity_keypair():
    """
    Generate the long-term cryptographic identity
    for a Hermes client.

    Returns:
        signing_private,
        signing_public,
        exchange_private,
        exchange_public,
    """

    signing_private = ed25519.Ed25519PrivateKey.generate()
    signing_public = signing_private.public_key()

    exchange_private = x25519.X25519PrivateKey.generate()
    exchange_public = exchange_private.public_key()

    return (
        signing_private,
        signing_public,
        exchange_private,
        exchange_public,
    )


def public_key_to_base64(public_key) -> str:
    raw = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    return base64.b64encode(raw).decode("ascii")


def base64_to_public_key(data: str, key_type: str):
    raw = base64.b64decode(data)
    if key_type == "ed25519":
        return (
            ed25519.Ed25519PublicKey
            .from_public_bytes(raw)
        )
    if key_type == "x25519":
        return (
            x25519.X25519PublicKey
            .from_public_bytes(raw)
        )
    raise ValueError("Unknown key type")


def generate_sender_key() -> bytes:
    return secrets.token_bytes(32)
