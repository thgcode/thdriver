from .client import Client
class LineReceiver(Client):
    """A client that receives lines."""
    buffer = ""
    encoding = "iso8859_1"

    def _dispatch_lines(self):
        b = self.buffer.find("\n")
        while b > -1:
            self.lineReceived(self.buffer[:b + 1])
            self.buffer = self.buffer[b + 1:]
            b = self.buffer.find("\n")

    def dataReceived(self, data):
        data = data.decode(self.encoding)
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
        return self.send((line + "\r\n").encode(self.encoding))
