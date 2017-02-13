.. _gettingstarted:


Getting started with ThDriver
===============================

ThDriver consists of three important objects: the client object that
handles the interaction with the client, the loop object that drives the
program and the server object that controls the accepting of connections
and the Internet data sending.

Since all of these actions must happen in one thread, you'll need to
design your program with special care so that it does not block waiting
for something to complete, because the main loop  would not have a chance to handle
the server.

Here is an example code that demonstrates some of ThDriver's
features::

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
