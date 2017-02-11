import time
class Log(object):
    def __init__(self, io):
        self.io = io

    def _format_message(self, message):
        mstring = time.ctime()
        mstring += ": "
        mstring += message
        return mstring + "\n"

    def write(self, message):
        self.io.write(self._format_message(message))

class LogManager(object):
    def __init__(self):
        self.logs = []

    def add_log(self, log):
        self.logs.append(log)

    def write(self, message):
        for l in self.logs:
            l.write(message)
