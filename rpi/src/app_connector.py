import json
from threading import Thread

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

DEFAULT_IP = "192.168.1.52"
DEFAULT_PORT = 4321


class AppConnector(object):
    def __init__(self):
        self.server = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # don't need to kill thread, because it is daemon thred
        if self.server:
            self.server.close()  # it closes all connections with clients as well

    def start_server(self):
        server_thread = Thread(target=self.create_server, daemon=True)
        server_thread.start()

    def create_server(self, ip=DEFAULT_IP, port=DEFAULT_PORT):
        self.server = SimpleWebSocketServer(ip, port, InfoWebSocket)
        self.server.serveforever()

    def send_points(self, dart_x, dart_y, segment):
        throw_info = {
            "x": dart_x,
            "y": dart_y,
            "segment": segment
        }
        message = json.dumps(throw_info)
        for client in self.server.connections.values():
            client.sendMessage(message)


class InfoWebSocket(WebSocket):

    def handleConnected(self):
        print(f"[INFO] WebSocket client {self.address} connected")

    def handleClose(self):
        print(f"[INFO] WebSocket client {self.address} disconnected")

