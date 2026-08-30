import secrets
import string
import threading
from datetime import datetime

class InviteManager:

    def __init__(self, interval: int = 60):
        self.interval = interval
        self.lastupdate = None
        self.current_code = None
        self.lock = threading.Lock()
        self.running = False
        self.thread = None

    def generate_code(self) -> str:
        alphabet = (string.ascii_uppercase + string.digits)
        return "".join(secrets.choice(alphabet) for _ in range(6))

    def rotate_code(self):
        new_code = self.generate_code()
        with self.lock:
            self.current_code = new_code
            self.lastupdate = datetime.now()
        print(f"[INVITE] [{self.lastupdate.strftime('%H:%M:%S')}] New invite code: {new_code}")

    def get_code(self) -> str | None:
        with self.lock:
            return self.current_code

    def validate_code(self, code: str) -> bool:
        if not code:
            return False

        with self.lock:
            return secrets.compare_digest(code.upper(),self.current_code or "")

    def _rotation_loop(self):
        while self.running:
            self.rotate_code()
            event = threading.Event()
            event.wait(self.interval)

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._rotation_loop,daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False