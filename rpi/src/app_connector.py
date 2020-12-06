import time
from datetime import datetime
from threading import Thread

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

client = None

class AppConnector(object):
    def __init__(self):
        # self.client = None
        self.server_thread = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # TODO: implement closing sockets, killing server and server_thread
        pass

    def start_server(self):
        self.server_thread = Thread(target=self.create_server)
        self.server_thread.start()

    def create_server(self):
        server = SimpleWebSocketServer('192.168.1.52', 4321, SimpleEcho)
        server.serveforever()

    def send_points(self, segment):
        global client
        client.sendMessage(str(segment))


class SimpleEcho(WebSocket):

    def handleConnected(self):
        print(self.address, 'connected')
        global client
        client = self

    def handleClose(self):
        print(self.address, 'closed')

