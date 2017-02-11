class Loop(object):
    def __init__(self):
        self.running = True
        self.callbacks = []

    def register_callback(self, type, function, *args, **kw):
        self.callbacks.append((type, function, args, kw))
        return len(self.callbacks) - 1

    def remove_callback(self, num):
        self.callbacks.remove(self.callbacks[num])

    def remove_callbacks(self, type):
        for c in self.callbacks:
            ctype = c[0]
            if type == ctype:
                self.callbacks.remove(c)

    def run_callbacks(self, ctype):
        result = True
        for c in self.callbacks:
            type, function, args, kw = c
            if type == ctype:
                res = function(*args, **kw)
                if not res:
                    result = False
        return result

    def run(self):
        if not self.run_callbacks("start"):
            print("Error: Initial callbacks can't run")
            return
        self.remove_callbacks("start") # Not necessary
        print("Entering main loop.")
        while self.running:
            self.running = self.run_callbacks("main")
        self.run_callbacks("shutdown")
