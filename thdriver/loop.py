class Loop(object):
    """This class drives all interaction between ThDriver and your
    program."""
    def __init__(self):
        self.running = True
        self.callbacks = []

    def register_callback(self, type, function, *args, **kw):
        """Registers a function to be called a certain time at the main
        loop.

        :param type: The type of the event that this function is to be
            registered
        :type type: str
        :param function: The function to be called
        :type function: function
        :returns: an identifier to unregister the callback
        :rtype: int"""
        self.callbacks.append((type, function, args, kw))
        return len(self.callbacks) - 1

    def remove_callback(self, identifier):
        """Removes the callback with the given identifier.

        :param identifier: The integer returned by the
            register_calback function
        :type identifier: int"""
        self.callbacks.remove(self.callbacks[identifier])

    def remove_callbacks(self, type):
        """Removes all the callbacks of the given type.

        :param type: The type of the callbacks
        :type type: str"""
        for c in self.callbacks:
            ctype = c[0]
            if type == ctype:
                self.callbacks.remove(c)

    def run_callbacks(self, type):
        """Runs callbacks of the specified type.

        :param type: The type of the callbacks to run
        :type type: str"""
        result = True
        for c in self.callbacks:
            ctype, cfunction, cargs, ckw = c
            if type == ctype:
                res = cfunction(*cargs, **ckw)
                if not res:
                    result = False
        return result

    def run(self):
        """Runs the main loop.

        First, the callbacks of the "start" type are run.

        After that, the main loop starts its job, running the callbacks
        in the "main" type.

        If one of these callbacks returns False, the main loop starts
        the shutdown process.

        In the shutdown process, the main loop runs the callbacks in
        the "shutdown" type and then terminates."""
        if not self.run_callbacks("start"):
            print("Error: Initial callbacks can't run")
            return
        self.remove_callbacks("start") # Frees used memory
        print("Entering main loop.")
        while self.running:
            self.running = self.run_callbacks("main")
        self.run_callbacks("shutdown")
