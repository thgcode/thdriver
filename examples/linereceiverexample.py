"""A server that sends welcome to the client and echoes all lines
received."""

from thdriver.linereceiver import LineReceiver
from thdriver.loop import Loop
from thdriver.server import Server

class LineEchoClient(LineReceiver):
    def connectionMade(self):
        self.sendLine("Welcome!")

    def lineReceived(self, line):
        self.sendLine(line)

if __name__ == "__main__":
    l = Loop()
    s = Server(l, "", 1963, cclass=LineEchoClient)
    l.run()
