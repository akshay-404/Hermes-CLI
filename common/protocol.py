import json


HEADER_SIZE = 4


def encode_packet(packet_type: str, payload: dict | None = None) -> bytes:
    packet = {
        "type": packet_type,
        "payload": payload or {}
    }

    data = json.dumps(packet).encode("utf-8")

    header = len(data).to_bytes(
        HEADER_SIZE,
        byteorder="big"
    )

    return header + data


def receive_packet(sock) -> dict:
    header = _receive_exact(sock, HEADER_SIZE)

    if not header:
        raise ConnectionError("Connection closed.")

    message_length = int.from_bytes(
        header,
        byteorder="big"
    )

    data = _receive_exact(
        sock,
        message_length
    )

    return json.loads(
        data.decode("utf-8")
    )


def _receive_exact(sock, length: int) -> bytes:
    data = bytearray()

    while len(data) < length:

        chunk = sock.recv(
            length - len(data)
        )

        if not chunk:
            raise ConnectionError(
                "Connection closed."
            )

        data.extend(chunk)

    return bytes(data)