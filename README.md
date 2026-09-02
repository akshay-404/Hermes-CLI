# Hermes CLI

Hermes CLI is a terminal-based chat application written in Python. It follows a client-server architecture and provides real-time communication through TCP sockets, with authentication, database management, and TLS-secured communication.

## Features

- Terminal-based chat interface
- Client-server architecture using TCP sockets
- User registration and authentication
- Invite-code based registration
- Real-time messaging
- Online-user status
- SQLite database with SQLAlchemy ORM
- TLS-secured client-server communication
- Structured JSON-based communication protocol
- Modular and extensible project architecture

## Project Structure

```text
Hermes/
├── client/
│   ├── ...
│   └── ...
├── server/
│   ├── ...
│   └── ...
├── common/
│   ├── protocol.py
│   ├── models.py
│   └── ...
├── tests/
│   └── ...
├── requirements.txt
└── README.md
```

The exact structure may change as the project develops.

## Architecture

Hermes uses a client-server architecture in which clients establish connections to a central server.

```text
+-------------+           TCP/TLS           +-------------+
|    Client   | <-------------------------> |    Server   |
+-------------+                             +-------------+
                                                  |
                                                  v
                                            SQLite Database
```

The client is responsible for the terminal interface and communication with the server. The server handles client connections, authentication, message routing, user management, and database operations.

## Network Communication

Hermes uses TCP sockets for reliable communication between clients and the server.

TLS is used to secure the connection between the client and server, providing confidentiality and integrity for data transmitted over the network.

The application uses a structured packet-based protocol built on top of the socket connection.

## Network Protocol

Hermes uses JSON packets for communication between clients and the server.

Packets contain a packet type and an associated payload.

Examples of packet types include:

```text
login
login_success
register
register_success
logout
logout_success
message
online
```

The protocol uses a fixed-size message header to indicate the size of the JSON payload that follows. This allows the receiver to determine where a complete packet ends, even when TCP delivers the data in multiple segments.

## Authentication

Users register and authenticate with the Hermes server using their account credentials.

Registration can also require a valid invite code, allowing access to the system to be controlled by the server.

## Database

Hermes currently uses SQLite with SQLAlchemy ORM.

The database is used to manage application data such as:

- User accounts
- Authentication information
- User public information
- Application state

SQLAlchemy provides an abstraction layer between the application and the underlying SQLite database.

## TLS

Hermes uses TLS to secure communication between clients and the server.

The TLS configuration uses certificates to establish the server's identity and protect network traffic from being read or modified by third parties during transmission.

For development and LAN deployments, the server certificate can be configured with the appropriate hostnames or IP addresses used by clients.

## Requirements

- Python 3.10 or newer
- SQLite
- A terminal capable of running the application
- OpenSSL/TLS certificate support

Python dependencies are listed in `requirements.txt`.

Install the dependencies with:

```bash
pip install -r requirements.txt
```

## Running Hermes

Clone the repository:

```bash
git clone https://github.com/akshay-404/Hermes-CLI.git
cd Hermes-CLI
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Initialize the database using the project's database initialization procedure.

Start the server:

```bash
python -m server.server
```

Start a client in another terminal:

```bash
python -m client.client
```

The exact entry-point paths may change as development continues.

## Configuration

Configuration such as the following should preferably be kept outside the source code:

- Server host and port
- Database location
- TLS certificate path
- TLS private key path
- Invite-code settings

Sensitive configuration files should not be committed to version control.

## Development

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


## Security

Hermes is currently a development and learning project. Although TLS is used to protect client-server communication, the overall application has not undergone an independent security audit.

Users should avoid relying on the current development version for highly sensitive communications.

## License

This project is currently unlicensed. A license will be added in a future release.
