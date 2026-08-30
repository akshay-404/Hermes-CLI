import ssl
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

CERT_FILE = (
    BASE_DIR.parent
    / "server"
    / "certs"
    / "server.crt"
)


def create_client_context() -> ssl.SSLContext:

    context = ssl.create_default_context(
        ssl.Purpose.SERVER_AUTH
    )

    context.minimum_version = ssl.TLSVersion.TLSv1_2

    context.load_verify_locations(
        cafile=CERT_FILE
    )

    return context