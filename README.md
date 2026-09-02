<p align="center">
<img src="assets/hermes-logo.png" alt="Hermes CLI Logo" width="622">
</p>
<p><h3 align="center">A terminal-based chat application written in Python</h3></p>

**_Hermes-CLI_** is a terminal-based chat application built using Python. It follows a client-server architecture and provides real-time communication through TCP sockets, with authentication, registration, database management, TLS-secured communication and customized terminal UI.


# Features

- Customized terminal-based UI
- Client-server architecture using TCP sockets
- User registration and authentication
- Invite-code based registration
- Real-time messaging
- Online-user status enquiry
- SQLite database with SQLAlchemy ORM
- TLS-secured client-server communication
- Structured JSON-based communication protocol
- Modular and extensible project architecture

# Project Structure

```text
Hermes-CLI/
├── assets
│   └── hermes-logo.png
├── client
│   ├── art.py
│   ├── client.py
│   ├── identity.py
│   ├── tls.py
│   └── ui.py
├── common
│   ├── __init.py__
│   ├── models.py
│   ├── protocol.py
├── database
│   ├── models.py
│   └── users.db
├── server
│   ├── auth.py
│   ├── certs
│   │   └── cert.conf.example
│   ├── database.py
│   ├── invite.py
│   ├── server.py
│   ├── socket_manager.py
│   └── tls.py
├── requirements.txt
├── tls-cert-gen.sh
└── README.md
```

The exact structure may change as the project develops.

# Architecture

Hermes uses a client-server architecture in which clients establish connections to a central server.

```text
+-------------+         TCP/TLS         +-------------+         TCP/TLS         +-------------+
|    Client   | <---------------------> |    Server   | <---------------------> |    Client   | 
+-------------+                         +-------------+                         +-------------+
                                               |
                                               v
                                         +------------+
                                         |  Database  |
                                         +------------+
```

The client is responsible for the terminal interface and communication with the server. The server handles client connections, authentication, message routing, user management, and database operations.

# Network Communication

Hermes uses TCP sockets for reliable communication between clients and the server. TLS is used to secure the connection between the client and server, providing confidentiality and integrity for data transmitted over the network. The application uses a structured packet-based protocol built on top of the socket connection.

# Network Protocol

Hermes uses JSON packets for communication between clients and the server. Packets contain a packet type and an associated payload. Examples of packet types include:

```text
login, login_success, register, register_success, logout, logout_success, message, online
```

The protocol uses a fixed-size message header to indicate the size of the JSON payload that follows. This allows the receiver to determine where a complete packet ends, even when TCP delivers the data in multiple segments.

# Authentication

Users register and authenticate with the Hermes server using their account credentials. Registration can also require a valid invite code, allowing access to the system to be controlled by the server.

# Database

Hermes currently uses SQLite with SQLAlchemy ORM. The database is used to manage application data such as user accounts, authentication information, user public information and application state. SQLAlchemy provides an abstraction layer between the application and the underlying SQLite database.

# Secure Communication (TLS)

Hermes uses TLS to secure communication between clients and the server. The TLS configuration uses certificates to establish the server's identity and protect network traffic from being read or modified by third parties during transmission. For development and LAN deployments, the server certificate can be configured with the appropriate hostnames or IP addresses used by clients.

# Deployment/Testing Hermes

Requirements include:
- Python 3.10 or newer
- SQLite
- A terminal capable of running the application
- OpenSSL/TLS certificate support
- Python dependencies listed in `requirements.txt`.


Clone the repository:

```bash
git clone https://github.com/akshay-404/Hermes-CLI.git
cd Hermes-CLI
```

Setup virtualenv and install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

TLS Certificate Setup:

Edit the `server/certs/cert.conf` to setup multiple SANs. Use `hermes.local` if using _mDNS_ or _Avahi_.

```bash
sudo chmod +x tls-cert-gen.sh
./tls-cert.gen.sh
```

Start the server:

```bash
python -m server.server
```
This starts the server and initialize the SQLite database.

Start a client in another terminal:

```bash
python -m client.client
```

Use localhost or hostname based on deployment mode. Use port 5000. The exact entry-point paths may change as development continues.

# Development

Hermes is currently under active development. The project is being developed incrementally, with networking, authentication, database management, TLS, and the terminal interface implemented as separate components.

Planned improvements include:

- End-to-end encryption
- Improved room and membership management
- Better message synchronization
- Additional error handling
- Improved logging
- Expanded test coverage
- Protocol refinement
- Additional security hardening
- Further improvements to the terminal interface


# License

This project is currently unlicensed. A license will be added in a future release.
