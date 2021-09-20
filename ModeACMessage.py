class ModeACMessage:
    def __init__(self, payload):
        self.payload = payload

    def __str__(self):
        s = "Mode A/C, payload ="
        for b in self.payload:
            s += " {:02x}".format(b)
        return s
