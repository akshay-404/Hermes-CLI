from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from socket import socket
from database.models import User

@dataclass
class Message:
    id: int
    sender_id: int
    ciphertext: str
    timestamp: datetime

@dataclass
class Session:
    user: User
    socket: socket
    connected_at: datetime