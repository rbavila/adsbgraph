from threading import Lock

class RangeRegister:
    def __init__(self):
        self.register = {
            "nw": 0,
            "ne": 0,
            "se": 0,
            "sw": 0
        }
        self.lock = Lock()

    def __reset(self):
        for k in self.register:
            self.register[k] = 0

    def __get(self):
        return (self.register["nw"], self.register["ne"],
            self.register["se"], self.register["sw"])

    def update(self, d, value):
        self.lock.acquire()
        if value > self.register[d]:
            self.register[d] = value
        self.lock.release()

    def get(self):
        self.lock.acquire()
        temp = self.__get()
        self.lock.release()
        return temp

    def resetget(self):
        self.lock.acquire()
        temp = self.__get()
        self.__reset()
        self.lock.release()
        return temp

if __name__ == "__main__":
    c = RangeRegister()
    print(c.get())
    c.update("nw", 10)
    print(c.get())
    c.update("se", 10)
    print(c.get())
    c.update("nw", 5)
    print(c.get())
    c.update("nw", 15)
    print(c.get())
    print(c.resetget())
    print(c.get())
