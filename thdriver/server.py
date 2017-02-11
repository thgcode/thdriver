from .client import Client
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE
from socket import socket
class Server(object):
    def __init__(self, loop, host=None, port=4000, cclass=Client):
        self.loop = loop
        self.selector = DefaultSelector()
        self.clients = []
        self.sock = socket()
        self._register_socket_for_select(self.sock)
        self.num_accepted = 0
        self.cclass = cclass
        if host is not None and port:
            self.loop.register_callback("start", self._start_server, host, port)
            self.loop.register_callback("shutdown", self._close_server)

    def _start_server(self, host, port):
        self.host = host
        self.port = port
        self.sock.bind((host, port))
        self._process_listening()
        self.loop.register_callback("main", self.check)
        self.loop.register_callback("main", self._process_listening)
        return True

    def _close_server(self):
        for c in self.clients[:]:
            c.close()
        self.sock.close()
        self.selector.close()
        return True

    def _process_listening(self):
        if self.num_accepted == 0:
            self.sock.listen(5)
            self.num_accepted = 5
        return True
    def _register_socket_for_select(self, socket):
        return self.selector.register(socket, EVENT_READ | EVENT_WRITE)

    def _unregister_socket_from_select(self, socket):
        return self.selector.unregister(socket)

    def _create_connection(self, sock, ip):
        client = self.cclass(self, sock, ip)
        self._register_socket_for_select(client)
        self.clients.append(client)

    def _accept_connection(self):
        self.num_accepted -= 1
        self._create_connection(*self.sock.accept())

    def check(self):
        for c, e in self.selector.select(0.001):
            if e & EVENT_READ:
                if c.fileobj is self.sock:
                    self._accept_connection()
                else:
                    c.fileobj._receive()
        for c in self.clients[:]:
            c._send()
        return True

    def client_crashed(self, client):
        self._unregister_socket_from_select(client)
        self.clients.remove(client)
