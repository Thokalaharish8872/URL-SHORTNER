import socket
try:
    sock = socket.create_connection(("localhost", 5432), timeout=2)
    print("Port 5432 is open")
    sock.close()
except Exception as e:
    print(f"Port 5432 is closed: {e}")
