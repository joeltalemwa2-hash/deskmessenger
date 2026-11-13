"""Interactive client for the TCP Help Desk Messenger."""
import json
import socket

HOST = "127.0.0.1"
PORT = 5050


def build_request(text):
    """Split user input into a command and optional argument."""
    if text is None:
        return {"command": "", "argument": ""}
    parts = str(text).strip().split(maxsplit=1)
    if not parts:
        return {"command": "", "argument": ""}
    return {"command": parts[0].upper(),
            "argument": parts[1] if len(parts) > 1 else ""}


def send_request(writer, request):
    """Serialize and send one request as a newline-delimited JSON object."""
    writer.write(json.dumps(request) + "\n")
    writer.flush()


def receive_response(reader):
    """Read one response line and convert it from JSON into a dictionary."""
    line = reader.readline()
    if not line:
        raise ConnectionError("The server closed the connection.")
    try:
        return json.loads(line)
    except json.JSONDecodeError as exc:
        raise ConnectionError("The server returned invalid JSON.") from exc


def display_response(response):
    """Print the message, data fields, and timestamp from a response."""
    if not isinstance(response, dict):
        print("\n[ERROR] The server returned an invalid response.")
        return
    status = "SUCCESS" if response.get("success") else "ERROR"
    print(f"\n[{status}] {response.get('message', 'No message')}")
    data = response.get("data", {})
    if isinstance(data, dict):
        for key, value in data.items():
            print(f"  {key.title()}: {value}")
    if response.get("timestamp"):
        print(f"  Time: {response['timestamp']}")


def show_instructions():
    """Display the commands supported by the help-desk server."""
    print("=" * 50)
    print("WELCOME TO THE TCP HELP DESK MESSENGER")
    print("Try HELP, STATUS, ECHO <message>, ADD <number> <number>, ")
    print("SUBTRACT <number> <number>, or EXIT.")
    print("=" * 50)


def run_client():
    """Connect to the server and exchange commands until the user exits."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    reader = None
    writer = None
    try:
        print(f"Connecting to {HOST}:{PORT}...")
        client.connect((HOST, PORT))
        print("Connected to the server.")
        reader = client.makefile("r", encoding="utf-8")
        writer = client.makefile("w", encoding="utf-8")
        show_instructions()
        while True:
            try:
                text = input("\nHelp Desk> ")
            except EOFError:
                print("\nInput closed. Exiting client.")
                break
            request = build_request(text)
            if not request["command"]:
                print("Enter a command. Type HELP for assistance.")
                continue
            try:
                send_request(writer, request)
                response = receive_response(reader)
                display_response(response)
            except (ConnectionError, OSError) as error:
                print(f"Communication error: {error}")
                break
            if request["command"] == "EXIT":
                break
        if reader is not None:
            reader.close()
        if writer is not None:
            writer.close()
    except ConnectionRefusedError:
        print("Connection refused. Start server.py first.")
    except OSError as error:
        print(f"[CLIENT ERROR] {error}")
    finally:
        client.close()
        print("Client connection closed.")


if __name__ == "__main__":
    run_client()
