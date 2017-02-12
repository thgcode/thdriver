import time
class Log(object):
    """Logs messages to an IO stream.

    :param io: The IO stream that this log is bound to
    :type io: file-like object"""
    def __init__(self, io):
        self.io = io

    def _format_message(self, message):
        mstring = time.ctime()
        mstring += ": "
        mstring += message
        return mstring + "\n"

    def write(self, message):
        """Logs the message to the IO stream.

        :param message: The message that is to be logged
        :type message: str"""
        self.io.write(self._format_message(message))

class LogManager(object):
    """A container for log objects."""
    def __init__(self):
        self.logs = []

    def add_log(self, log):
        """Adds a log object to the manager.

        :param log: The log object that is to be added
        :type log: thdriver.log.Log instance"""
        self.logs.append(log)

    def write(self, message):
        """Writes the messages to all the log instances on the manager.

        :param message: The message that is to be written
        :type message: str"""
        for l in self.logs:
            l.write(message)
