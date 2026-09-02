import secrets
from dataclasses import dataclass
from common.crypto import generate_sender_key
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


class SenderKey:
    """
    Symmetric sender-key chain for one user in one room.
    """

    def __init__(self, chain_key: bytes | None = None):
        self.chain_key = (
            chain_key
            if chain_key is not None
            else generate_sender_key()
        )
        self.message_index = 0

    def _derive(self, key: bytes, info: bytes,) -> bytes:
        return HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=info,
        ).derive(key)

    def next_message_key(self) -> tuple[bytes, int]:
        message_key = self._derive(
            self.chain_key,
            b"Hermes Sender Key Message",
        )
        self.chain_key = self._derive(
            self.chain_key,
            b"Hermes Sender Key Chain",
        )
        index = self.message_index
        self.message_index += 1
        return message_key, index


@dataclass
class SenderKeyState:
    sender: str
    room_id: str
    key_id: str
    chain_key: bytes
    message_index: int = 0
