from .client import Client
class LineReceiver(Client):
    buffer = ""

    def _dispatch_lines(self):
        lst = self.buffer.split("\n")
        for l in lst:
            self.lineReceived(l.strip())
        self.buffer = ""

    def dataReceived(self, data):
        data = data.decode("iso8859_1")
        if data.find("\n") > -1:
            self.buffer += data
            self._dispatch_lines() # Problem when several lines are received
        else:
            self.buffer += data

    def lineReceived(self, line):
        pass

    def sendLine(self, line):
        return self.send(line + "\r\n")
