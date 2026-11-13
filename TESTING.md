# Testing Guide

1. Open a terminal in this folder and run `python server.py`.
2. Open a second terminal and run `python client.py`.
3. Test the following commands:

| Input | Expected result |
|---|---|
| HELP | Lists supported commands |
| STATUS | Reports server online, host, and port |
| ECHO Hello Joel | Returns the supplied message |
| ECHO | Asks for a message |
| ADD 10 5 | Returns 15 |
| SUBTRACT 20 7 | Returns 13 |
| UNKNOWN | Reports an unknown command |
| EXIT | Sends goodbye and closes the session |

To test an unavailable server, stop it with CTRL+C and run the client. It should report that the connection was refused.

To test multiple clients, leave the server running and start clients in two terminals. The server creates a separate thread for each client.

The default `127.0.0.1` host is for testing on one computer. A two-computer test requires a reachable server network interface and the server computer's LAN IP address.
