import pyModeS

class ModeSMessage:
    def __init__(self, raw):
        self.raw = raw
        self.hex = raw.hex()
        self.__decode()

    def __decode(self):
        self.df = pyModeS.df(self.hex)
        self.icao = pyModeS.icao(self.hex).upper()
        if self.is_adsb():
            self.tc = pyModeS.adsb.typecode(self.hex)
            if self.has_callsign():
                self.callsign = pyModeS.adsb.callsign(self.hex).strip('_')

    def __str__(self):
        s = "Mode S"
        s += ", df = {:02}".format(self.df)
        if self.icao is not None:
            s += ", icao = " + self.icao
        if self.is_adsb():
            if self.has_callsign():
                s += ", callsign = " + self.callsign
        s += ", hex = " + self.hex
        return s

    def is_adsb(self):
        return self.df == 17

    def has_callsign(self):
        return 1 <= self.tc <= 4

    def has_position(self):
        return 5 <= self.tc <= 18 or 20 <= self.tc <= 22

    def oe_flag(self):
        return pyModeS.decoder.adsb.oe_flag(self.hex)
