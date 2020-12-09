import socket

DEFAULT_IP = "192.168.1.52"
DEFAULT_PORT = 1235


class ServerConnector(object):

    def __init__(self):
        self.s = None
        self.conn = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            print("[INFO] Closing the connection")
            self.conn.close()
        if self.s:
            print("[INFO] Closing the socket")
            self.s.close()

    def create_server_and_wait_for_client(self, ip=DEFAULT_IP, port=DEFAULT_PORT):
        """

            Creates server socket, binds to IP address and waits (blocking)
            for incoming client connection.

            Arguments:
                ip      server ip to bind to
                port    server port to bind to

            Returns tuple (socket, connection).
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((ip, port))
        s.listen()
        conn, _ = s.accept()
        self.s = s
        self.conn = conn

    def receive_throw_info(self):
        """
            Waits (blocking) and receives info about one throw. Needs to be compatible with send_throw_info().

            Arguments:
                conn    connection with client

            Returns tuple (counter, x, y).
        """
        data = self.conn.recv(3 * 4)
        if not data:
            print("[ERROR] Client disconnected")
            raise ConnectionError()
        counter = int.from_bytes(data[:4], byteorder="big")
        x = int.from_bytes(data[4:8], byteorder="big")
        y = int.from_bytes(data[8:12], byteorder="big")
        return counter, x, y


class ClientConnector(object):

    def __init__(self):
        self.s = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.s:
            print("[INFO] Closing the socket")
            self.s.close()

    def connect_client_to_server(self, ip=DEFAULT_IP, port=DEFAULT_PORT):
        """
            Creates client socket and tries to connect to server.

            Arguments:
                ip      server ip
                port    server port
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        self.s = s

    def send_throw_info(self, counter: int, x: int, y: int):
        """
            Sends info about one throw.
            It contains counter of throw and x, y pixels coords of landing point of throw.
            Each element is sent as 4 bytes integer in big endian order.

            Order is: [counter, x, y].

            Arguments:
                s           server socket
                counter     no. of throw
                x           horizontal position of throw in pixels
                y           vertical position of throw in pixels
        """
        counter = int(counter).to_bytes(4, byteorder="big")
        x = int(x).to_bytes(4, byteorder="big")
        y = int(y).to_bytes(4, byteorder="big")
        throw_info = bytes(counter + x + y)
        self.s.send(throw_info)
