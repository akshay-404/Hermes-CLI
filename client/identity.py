from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519, x25519
from common.crypto import generate_identity_keypair

IDENTITY_DIR = Path.home() / ".hermes"

SIGNING_PRIVATE_FILE = IDENTITY_DIR / "identity_ed25519.key"
EXCHANGE_PRIVATE_FILE = IDENTITY_DIR / "identity_x25519.key"


class Identity:

    def __init__(
        self,
        signing_private: ed25519.Ed25519PrivateKey,
        exchange_private: x25519.X25519PrivateKey,
    ):
        self.signing_private = signing_private
        self.signing_public = signing_private.public_key()

        self.exchange_private = exchange_private
        self.exchange_public = exchange_private.public_key()

    def save(self):
        IDENTITY_DIR.mkdir(
            mode=0o700,
            exist_ok=True
        )
        signing_bytes = self.signing_private.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption(),
        )
        exchange_bytes = self.exchange_private.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption(),
        )
        SIGNING_PRIVATE_FILE.write_bytes(signing_bytes)
        EXCHANGE_PRIVATE_FILE.write_bytes(exchange_bytes)
        SIGNING_PRIVATE_FILE.chmod(0o600)
        EXCHANGE_PRIVATE_FILE.chmod(0o600)

    @classmethod
    def load(cls):
        signing_bytes = SIGNING_PRIVATE_FILE.read_bytes()
        exchange_bytes = EXCHANGE_PRIVATE_FILE.read_bytes()
        signing_private = (
            ed25519.Ed25519PrivateKey.from_private_bytes(
                signing_bytes
            )
        )
        exchange_private = (
            x25519.X25519PrivateKey.from_private_bytes(
                exchange_bytes
            )
        )
        return cls(
            signing_private,
            exchange_private
        )


def load_or_create_identity():
    if (
        SIGNING_PRIVATE_FILE.exists()
        and EXCHANGE_PRIVATE_FILE.exists()
    ):
        return Identity.load()
    (
        signing_private, _,
        exchange_private, _,
    ) = generate_identity_keypair()

    identity = Identity(signing_private, exchange_private)
    identity.save()
    return identity
