"""Echo server example."""

from thdriver.client import Client
from thdriver.loop import Loop
from thdriver.server import Server
class EchoClient(Client):
    def dataReceived(self, data):
        self.send(data)

if __name__ == "__main__":
    l = Loop()
    s = Server(l, "", 1963, cclass=EchoClient)
    l.run()
