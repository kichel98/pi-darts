import socket

DEFAULT_IP = "192.168.1.51"
DEFAULT_PORT = 1234


def create_server_and_wait_for_client(ip=DEFAULT_IP, port=DEFAULT_PORT):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((ip, port))
        s.listen()
        conn, _ = s.accept()
        return s, conn
    except:
        s.close()


def connect_client_to_server():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("192.168.1.51", 1234))
        return s
    except:
        s.close()


def send_dart_info(s, counter: int, x: int, y: int):
    counter = int(counter).to_bytes(4, byteorder="big")
    x = int(x).to_bytes(4, byteorder="big")
    y = int(y).to_bytes(4, byteorder="big")
    dart_info = bytes(counter + x + y)
    s.send(dart_info)


def receive_dart_info(conn):
    data = conn.recv(3 * 4)
    if not data:
        # TODO: check if data is not 0 (can occurs after disconnect)
        print("[ERROR] Client disconnected")
        return ConnectionError()
    print("New data from Pi Zero!")
    counter = int.from_bytes(data[:4], byteorder="big")
    x = int.from_bytes(data[4:8], byteorder="big")
    y = int.from_bytes(data[8:12], byteorder="big")
    return counter, x, y
