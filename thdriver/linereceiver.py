from .client import Client
class LineReceiver(Client):
    """A client that receives lines."""
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
        """A line of text was received.

        :param line: The line that was received
        :type line: str"""
        pass

    def sendLine(self, line):
        """Sends a line of text to the client

        :param line: The line that is to be sent
        :type line: str"""
        return self.send((line + "\r\n").encode("iso8859_1"))
