import socket
class Client(object):
    """Class that represents the connection with a internet client."""
    def __init__(self, server, sock, ip):
        """Creates the class.

        :param server: server.server instance
        :param socket: socket.socket instance
        :param ip: The IP of the socket, a tuple of (host, port).
        """
        self.server = server
        self.sock = sock
        self.ip = ip
        self.crash = False
        self.data_buffer = b""
        self.connectionMade()

    def connectionMade(self):
        """Indicates that a connection was made to this client.
        Needs to be subclassed."""
        pass

    def connectionLost(self, reazon):
        """The connection with the client wass lost.
        Needs to be subclassed.

        :param reazon: Why the connection was lost
        :type reazon: str
        """
        pass

    def fileno(self):
        """Return the fileno() of the socket object used internally.

        :rtype: int
        """
        return self.sock.fileno()

    def dataReceived(self, data):
        """Some data was received by the client.
        Needs to be subclassed.

        :param data: What whas received
        :type data: bytes
        """
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
        """Indicates that the connection with the client was crashed."""
        if not self.crash:
            self.crash = True
            self.server.client_crashed(self)
            self.connectionLost("Connection down")

    def _send(self):
        if not self.crash:
            if len(self.data_buffer) > 1024:
                b = self.data_buffer[:1024]
                self.data_buffer = self.data_buffer[1024:]
            else:
                b = self.data_buffer
                self.data_buffer = b""
            try:
                return self.sock.sendall(b)
            except socket.error:
                self.crashed()

    def send(self, data):
        """Sends data to the client.

        :param data: What is to be sent
        :type data: bytes
        """
        self.data_buffer += data

    def close(self):
        """Closes the socket."""
        self.sock.close()
        self.crashed() # Indirectly crash

    @property
    def factory(self): # For twisted
        return self.server
