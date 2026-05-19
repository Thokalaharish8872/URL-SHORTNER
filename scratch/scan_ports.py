import socket
for port in range(5430, 5445):
    try:
        sock = socket.create_connection(("127.0.0.1", port), timeout=0.1)
        print(f"Port {port} is OPEN")
        sock.close()
    except:
        pass
