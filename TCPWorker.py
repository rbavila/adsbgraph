import threading
import socket
from queue import SimpleQueue
import sys
import time

class TCPWorker(threading.Thread):
    def __init__(self, host, port):
        super().__init__(name = "TCPWorker", daemon = True)
        self.hostport = (host, port)
        self.server = socket.create_connection(self.hostport)
        self.buffer = SimpleQueue()

    def run(self):
        while True:
            msg = self.server.recv(1024)
            if not msg:
                self.__try_reconnect()
                continue
            for b in msg:
                self.buffer.put(b)

    def __try_reconnect(self):
        print("Connection lost, trying to reconnect...", file=sys.stderr)
        self.server = None
        while not self.server:
            try:
                self.server = socket.create_connection(self.hostport)
            except:
                print("Reconnection failed, trying again...", file=sys.stderr)
                time.sleep(2)
                self.server = None
        print("Ok, good to go!", file=sys.stderr)
