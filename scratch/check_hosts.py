import socket
def check(host, port):
    try:
        sock = socket.create_connection((host, port), timeout=2)
        print(f"{host}:{port} is OPEN")
        sock.close()
    except Exception as e:
        print(f"{host}:{port} is CLOSED: {e}")

check("127.0.0.1", 5432)
check("localhost", 5432)
check("::1", 5432)
