import socket
class Client(object):
    def __init__(self, server, sock, ip):
        self.server = server
        self.sock = sock
        self.ip = ip
        self.crash = False
        self.data_buffer = ""
        self.connectionMade()

    def connectionMade(self):
        pass

    def connectionLost(self, reazon):
        pass

    def fileno(self):
        """Return the fileno() of the socket object used internally."""
        return self.sock.fileno()

    def dataReceived(self, data):
        pass

    def _receive(self):
        try:
            data = self.sock.recv(4096)
        except socket.error:
            self.crashed()
        else:
            if data:
                return self.dataReceived(data)
            else:
                self.crashed()

    def crashed(self):
        if not self.crash:
            self.crash = True
            self.server.client_crashed(self)
            self.connectionLost("Connection down")

    def _send(self):
        if not self.crash:
            if len(self.data_buffer) > 1024:
                b = self.data_buffer[:1024]
                self.data_buffer = self.buffer[1024:]
            else:
                b = self.data_buffer
                self.data_buffer = ""
            try:
                return self.sock.sendall(b.encode("iso8859_1"))
            except socket.error:
                self.crashed()

    def send(self, data):
        self.data_buffer += data

    def close(self):
        self.sock.close()
        self.crashed() # Indirectly crash

    @property
    def factory(self): # For twisted
        return self.server
