import threading

from common.models import Session


class SocketManager:

    def __init__(self):
        self.sessions: dict[str, Session] = {}
        self.lock = threading.Lock()

    def add_session(self, session: Session) -> bool:
        username = session.user.username
        with self.lock:
            if username in self.sessions:
                return False
            self.sessions[username] = session
        return True

    def remove_session(self, username: str):
        with self.lock:
            self.sessions.pop(username, None)

    def get_session(self, username: str) -> Session | None:
        with self.lock:
            return self.sessions.get(username)

    def get_online_users(self) -> list[str]:
        with self.lock:
            return list(self.sessions.keys())

    def broadcast(self, data: bytes):
        with self.lock:
            sessions = list(self.sessions.items())
        disconnected = []
        for username, session in sessions:
            try:
                session.socket.sendall(data)
            except (ConnectionResetError, BrokenPipeError, OSError):
                disconnected.append(username)
        for username in disconnected:
            self.remove_session(username)
