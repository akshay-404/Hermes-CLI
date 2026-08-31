import socket
import threading
import sys
import ssl
from client.art import ASCII_color, ASCII_plain
from client.tls import create_client_context
from client.ui import ChatUI
from datetime import datetime
from common.protocol import encode_packet, receive_packet

print(ASCII_color)

SERVER = input("Enter server address [<address> <port>] : ")
try:
    SERVER_HOST, SERVER_PORT = SERVER.split(' ')
except:
    print("Incorrect syntax or server does not exist !!!")
    sys.exit()

ui = ChatUI()

authenticated = False
username = None

def receive_messages(sock):
    global authenticated
    global username

    try:
        while True:
            packet = receive_packet(sock)
            packet_type = packet.get("type")
            payload = packet.get("payload", {})

            if packet_type == "message":
                sender = payload.get("username")
                message = payload.get("message")
                timestamp = payload.get("timestamp")
                isself = sender == username
                ui.print_message(sender, message, timestamp, isself)

            elif packet_type == "login_success":
                authenticated = True
                username = payload.get("username")
                ui.set_username(username)
                ui.print_info(f"[+] Logged in as: {username}")

            elif packet_type == "login_fail":
                authenticated = False
                username = payload.get("username")
                ui.print_info(f"[!] Login failed: {payload.get('message')}")

            elif packet_type == "register_success":
                ui.print_info("[+] Registration successful.")
                ui.print_system("Use /login to enter the chat." + "\n")

            elif packet_type == "register_fail":
                username = payload.get("username")
                ui.print_info(
                    f"[!] Registration failed: {payload.get('message')}")

            elif packet_type == "logout_success":
                authenticated = False
                username = None
                ui.set_username(username)
                ui.print_info("[-] Logged out.")
                ui.print_system("\n")

            elif packet_type == "online":
                users = payload.get("users", [])
                ui.print_info(f"[] Online users: {' '.join(users)}")

            elif packet_type == "message":
                sender = payload.get("username")
                message = payload.get("message")
                timestamp = payload.get("timestamp")
                isself = sender == username
                ui.print_message(sender, message, timestamp, isself)

    except ConnectionError:
        ui.print_info("[-] Disconnected from server.")
        sys.exit()


def send_command(sock, packet_type, payload):
    sock.sendall(encode_packet(packet_type, payload))


def handle_input(sock, instr, data):
    global authenticated
    if instr == "default":
        command = data
        if not command:
            return

        if command.startswith("/") and not command.startswith("//"):
            if command == "/online":
                if not authenticated:
                    ui.print_info("[!] You must login first.")
                    return
                send_command(sock, "online", {})

            elif command == "/logout":
                if not authenticated:
                    ui.print_info("[!] You are not logged in.")
                    return
                send_command(sock, "logout", {})

            elif command == "/quit":
                if authenticated:
                    send_command(sock, "logout", {})
                sock.close()
                sys.exit()

            elif command == "/help":
                ui.print_info(
                    "[!] Available commands: /register /login /logout /online /quit")

            elif command == "/login":
                if authenticated:
                    ui.print_info("[!] You are already logged in.")
                    return
                ui.show_login()

            elif command == "/register":
                if authenticated:
                    ui.print_info("[!] Logout before registering.")
                    return
                ui.show_register()

            else:
                ui.print_info("[!] Unknown command. Use /help")

        else:
            if not authenticated:
                ui.print_info("[!] You must login first.")
                return
            message = command[1:] if command.startswith("//") else command
            send_command(sock, "message",
                         {"message": message}
                         )

    elif instr == "login":
        if authenticated:
            ui.print_info("[!] You are already logged in.")
            return
        send_command(sock, "login", data)

    elif instr == "register":
        if authenticated:
            ui.print_info("[!] Logout before registering.")
            return
        send_command(sock, "register", data)


def start_client():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = create_client_context()
    tls_socket = context.wrap_socket(sock, server_hostname=SERVER_HOST)

    try:
        tls_socket.connect((SERVER_HOST, int(SERVER_PORT)))
        ui.print_system(ASCII_plain)
        ui.print_system(
            f"[+] Connected to chat server at {SERVER_HOST}:{SERVER_PORT}")
        ui.print_system("[+] Type /help to display available commands." + "\n")

        receiver_thread = threading.Thread(
            target=receive_messages, args=(tls_socket,), daemon=True)
        receiver_thread.start()

        ui.set_input_callback(
            lambda instr, data: handle_input(tls_socket, instr, data)
        )
        ui.run()

    except TimeoutError:
        print(
            f"[!] Could not connect to server. Is the server running on  {SERVER_HOST}?")

    except ConnectionRefusedError:
        print(
            f"[!] Could not connect to server. Is the server running on port {SERVER_PORT}?")

    except ssl.SSLError as e:
        print(f"[!] TLS error: {e}")

    finally:
        tls_socket.close()


if __name__ == "__main__":
    start_client()
