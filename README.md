# Overview

The Python TCP Client-Server Help Desk Messenger demonstrates communication between two programs using the client-server model. The client sends requests and the server processes them and returns responses.

Commands:
- `HELP` lists available commands.
- `STATUS` reports whether the server is online.
- `ECHO <message>` returns the supplied message.
- `ADD <number> <number>` adds two numbers and returns the result.
- `SUBTRACT <number> <number>` subtracts the second number from the first and returns the result.
- `EXIT` closes the client session.

Open two terminals in this folder. Run `python server.py` in the first terminal, then `python client.py` in the second. Enter commands at the client prompt.

The purpose of this project is to practise TCP socket programming, understand client-server architecture, and learn how applications exchange structured messages.

[Software Demo Video](VIDEO_LINK_TO_BE_ADDED)

# Network Communication

The project uses a client-server architecture. The server waits for incoming connections. The client initiates a connection, sends a request, and displays the server response.

The transport protocol is TCP. The server listens on port **5050**. The host is `127.0.0.1` for local testing. For testing across computers, configure the server to listen on a reachable network interface and set the client host to the server computer's LAN IP address.

Messages use JSON, with one JSON object per line. Requests contain `command` and `argument`. Responses contain `success`, `message`, `data`, and `timestamp`. A newline marks the end of each message.

# Development Environment

The project uses Python 3 and Visual Studio Code on Windows. It uses standard-library modules:
- `socket` for TCP connections.
- `threading` for handling multiple clients.
- `json` for structured messages.
- `datetime` for response timestamps.

No third-party packages are required.

# Useful Websites

- [Python Socket Documentation](https://docs.python.org/3/library/socket.html)
- [Python Threading Documentation](https://docs.python.org/3/library/threading.html)
- [Python JSON Documentation](https://docs.python.org/3/library/json.html)
- [BYU-I CSE310 Networking Module](https://byui-cse.github.io/cse310-ww-course/modules/module_descriptions.html)
- [GitHub Documentation](https://docs.github.com/)

# Future Work

- Add user authentication.
- Store help-desk requests in a database.
- Add a graphical user interface.
- Add TLS encryption for use beyond local learning tests.
- Add automated tests for simultaneous clients.
