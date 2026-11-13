"""TCP Help Desk Messenger server using newline-delimited JSON over TCP."""
import json
import socket
import threading
from datetime import datetime


def normalize_number(value):
    """Return an int when a float is mathematically whole; otherwise keep the float."""
    number = float(value)
    if number.is_integer():
        return int(number)
    return number


def parse_numeric_pair(argument):
    """Parse two numeric values from a command argument."""
    parts = argument.strip().split()
    if len(parts) != 2:
        raise ValueError(
            "Use format ADD <number> <number> or SUBTRACT <number> <number>."
        )
    try:
        return float(parts[0]), float(parts[1])
    except ValueError as exc:
        raise ValueError("Both values must be valid numbers.") from exc

HOST = "127.0.0.1"
PORT = 5050


def make_response(success, message, data=None):
    """Create a standard response dictionary for the client."""
    return {"success": success,
            "message": message,
            "data": data if isinstance(data, dict) else {},
            "timestamp": datetime.now().isoformat(timespec="seconds")}


def handle_command(command, argument=""):
    """Process one supported help-desk command and return its response."""
    command = command.strip().upper()
    if command == "HELP":
        return make_response(
            True,
            "Commands: HELP, STATUS, ECHO <message>, ADD <number> <number>, SUBTRACT <number> <number>, EXIT.")
    if command == "STATUS":
        return make_response(True, "Server is online.",
                             {"status": "online", "host": HOST, "port": PORT})
    if command == "ECHO":
        if not argument.strip():
            return make_response(False, "Please provide a message after ECHO.")
        return make_response(True, f"Server received: {argument}")
    if command == "ADD":
        try:
            left, right = parse_numeric_pair(argument)
        except ValueError as error:
            return make_response(False, str(error))
        result = normalize_number(left + right)
        return make_response(
            True,
            f"{normalize_number(left)} + {normalize_number(right)} = {result}",
            {"operation": "addition", "first_number": normalize_number(left),
             "second_number": normalize_number(right), "result": result},
        )
    if command == "SUBTRACT":
        try:
            left, right = parse_numeric_pair(argument)
        except ValueError as error:
            return make_response(False, str(error))
        result = normalize_number(left - right)
        return make_response(
            True,
            f"{normalize_number(left)} - {normalize_number(right)} = {result}",
            {"operation": "subtraction", "first_number": normalize_number(left),
             "second_number": normalize_number(right), "result": result},
        )
    if command == "EXIT":
        return make_response(True, "Goodbye. Closing your connection.")
    return make_response(False, f"Unknown command: {command}. Type HELP.")


def send_response(writer, response):
    """Send one JSON response line to the connected client."""
    writer.write(json.dumps(response) + "\n")
    writer.flush()


def receive_request(reader):
    """Read and decode one JSON request line from the client."""
    line = reader.readline()
    if not line:
        return None
    try:
        return json.loads(line)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON request.")


def handle_client(connection, address):
    """Handle requests from one client until it disconnects or sends EXIT."""
    print(f"[CONNECTED] {address}")
    reader = connection.makefile("r", encoding="utf-8")
    writer = connection.makefile("w", encoding="utf-8")
    try:
        while True:
            try:
                request = receive_request(reader)
                if request is None:
                    break
                if not isinstance(request, dict):
                    raise ValueError("Request must be a JSON object.")
                command = str(request.get("command", ""))
                argument = str(request.get("argument", ""))
                print(f"[REQUEST] {address}: {command} {argument}")
                response = handle_command(command, argument)
                send_response(writer, response)
                if command.strip().upper() == "EXIT":
                    break
            except ValueError as error:
                send_response(writer, make_response(False, str(error)))
            except (ConnectionError, OSError) as error:
                print(f"[CLIENT ERROR] {address}: {error}")
                break
    finally:
        reader.close()
        writer.close()
        connection.close()
        print(f"[DISCONNECTED] {address}")


def start_server():
    """Start listening for TCP connections and serve clients in threads."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((HOST, PORT))
        server.listen()
        print("=" * 50)
        print("PYTHON TCP HELP DESK MESSENGER")
        print(f"Listening on {HOST}:{PORT}")
        print("Press CTRL+C to stop.")
        print("=" * 50)
        while True:
            connection, address = server.accept()
            thread = threading.Thread(target=handle_client,
                                      args=(connection, address), daemon=True)
            thread.start()
    except KeyboardInterrupt:
        print("\nServer shutdown requested.")
    except OSError as error:
        print(f"[SERVER ERROR] {error}")
    finally:
        server.close()
        print("Server socket closed.")


if __name__ == "__main__":
    start_server()
