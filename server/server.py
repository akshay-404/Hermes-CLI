import socket
import threading
import ssl
from datetime import datetime
from common.models import Session
from common.protocol import encode_packet, receive_packet
from server.auth import login_user, register_user
from server.database import initialize_database
from server.socket_manager import SocketManager
from server.invite import InviteManager
from server.tls import create_server_context


def localip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
        except OSError:
            return "127.0.0.1"

HOST = "0.0.0.0"
PORT = 5000

socket_manager = SocketManager()
invite_manager = InviteManager(interval=60)

def send_packet(client_socket: socket.socket, packet_type: str, payload: dict | None = None):
    client_socket.sendall(encode_packet(packet_type, payload))


def handle_client(client_socket: socket.socket, address):
    session = None
    try:
        while True:
            packet = receive_packet(client_socket)
            packet_type = packet.get("type")
            payload = packet.get("payload", {})

            if packet_type == "login":
                if session is not None:
                    send_packet(
                        client_socket,
                        "login_success",
                        {"message": "Already logged in."}
                    )
                    continue

                username = payload.get("username")
                password = payload.get("password")
                if not username or not password:
                    send_packet(
                        client_socket,
                        "login_fail",
                        {"message": "Username and password required."}
                    )
                    continue

                user = login_user(username, password)
                if user is None:
                    send_packet(
                        client_socket,
                        "login_fail",
                        {"message": "Invalid username or password."}
                    )
                    continue

                if socket_manager.get_session(user.username) is not None:
                    send_packet(
                        client_socket,
                        "login_fail",
                        {"message": "User already online."}
                    )
                    continue

                session = Session(user=user, socket=client_socket,
                                  connected_at=datetime.now())
                socket_manager.add_session(session)
                send_packet(
                    client_socket,
                    "login_success",
                    {"username": user.username}
                )
                print(f"[+] {user.username} logged in")

            elif packet_type == "online":
                if session is None:
                    continue
                send_packet(
                    client_socket,
                    "online",
                    {"users": socket_manager.get_online_users()}
                )

            elif packet_type == "register":
                username = payload.get("username").strip()
                password = payload.get("password")
                invite = payload.get("invite")
                if not invite_manager.validate_code(invite):
                    send_packet(
                        client_socket,
                        "register_fail",
                        {"message": "Invalid or expired invite code."}
                    )
                    continue
                try:
                    user = register_user(username, password)
                    send_packet(
                        client_socket,
                        "register_success",
                        {"username": user.username}
                    )
                    print(f"[+] Registered user: {user.username}")
                except ValueError as e:
                    send_packet(
                        client_socket,
                        "register_fail",
                        {"message": str(e)}
                    )

            elif packet_type == "message":
                if session is None:
                    continue
                message = payload.get("message")
                if not message:
                    continue
                username = (session.user.username)

                socket_manager.broadcast(
                    encode_packet(
                        "message",
                        {"username": username, "message": message, "timestamp": datetime.now().strftime("%H:%M:%S")}
                    )
                )

            elif packet_type == "logout":
                if session is None:
                    send_packet(
                        client_socket,
                        "logout_fail",
                        {"message": "Not logged in."}
                    )
                    continue

                username = (session.user.username)
                socket_manager.remove_session(username)
                session = None

                send_packet(
                    client_socket,
                    "logout_success"
                )
                print(f"[-] {username} logged out")

            else:
                print(f"[!] Unknown packet type: {packet_type}")

    except ConnectionError:
        print(f"[-] Connection closed: {address}")

    except Exception as e:
        print(f"[!] Error with {address}: {e}")

    finally:
        if session is not None:
            username = (session.user.username)
            socket_manager.remove_session(username)
            print(f"[-] {username} disconnected")
        client_socket.close()


def start_server():
    initialize_database()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    tls_context = create_server_context()
    
    print(f"[*] Chat server listening on {localip()}:{PORT}")

    invite_manager.start()

    while True:
        client_socket, address = server_socket.accept()
        print(f"[+] TCP connection from {address}")

        try:
            tls_socket = tls_context.wrap_socket(client_socket, server_side=True)
            print(f"[+] TLS connection established with {address}")

        except ssl.SSLError as e:
            print(f"[!] TLS handshake failed with {address}: {e}")
            client_socket.close()
            continue

        client_thread = threading.Thread(
            target=handle_client,
            args=(tls_socket, address),
            daemon=True
        )

        client_thread.start()


if __name__ == "__main__":
    start_server()