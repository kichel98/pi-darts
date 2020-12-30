import json
from threading import Thread

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

DEFAULT_IP = "192.168.1.52"
DEFAULT_PORT = 4321


class AppConnector(object):
    """
        Manages connections with client (mobile) apps.
    """
    def __init__(self):
        self.server = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # don't need to kill thread, because it is daemon thread
        if self.server:
            self.server.close()  # it closes all connections with clients as well

    def start_server(self):
        """
            Prepares new daemon server thread and starts it.
        """
        server_thread = Thread(target=self.create_server, daemon=True)
        server_thread.start()

    def create_server(self, ip=DEFAULT_IP, port=DEFAULT_PORT):
        """
            Creates WebSocket server and starts infinite listening.

            Arguments:
                 ip     ip number at which server will listen
                 port   port at which server will listen
        """
        self.server = SimpleWebSocketServer(ip, port, InfoWebSocket)
        self.server.serveforever()

    def send_points(self, dart_x, dart_y, segment):
        """
            Sends info about throw to all clients.

            Arguments:
                dart_x      first coord of dart position
                dart_y      second coord of dart position
                segment     segment mapped to throw
        """
        throw_info = {
            "x": dart_x,
            "y": dart_y,
            "segment": segment
        }
        message = json.dumps(throw_info)
        for client in self.server.connections.values():
            client.sendMessage(message)


class InfoWebSocket(WebSocket):
    """
        Derived class of WebSocket (from SimpleWebSocketServer), which defined callbacks,
        called at specific moments of connection lifecycle.
    """
    def handleConnected(self):
        print(f"[INFO] WebSocket client {self.address} connected")

    def handleClose(self):
        print(f"[INFO] WebSocket client {self.address} disconnected")

