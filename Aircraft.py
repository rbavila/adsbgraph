import time
import pyModeS
from Position import Position

class Aircraft:
    def __init__(self, icao):
        self.icao = icao
        self.callsign = None
        self.position = None
        self.lastseen = 0
        self.msg_count = 0
        self.tsmsg0 = None
        self.tsmsg1 = None

    def __str__(self):
        s = self.icao
        if self.lastseen > 0:
            s += ", lastseen " + time.ctime(self.lastseen)
        if self.callsign is not None:
            s += ", " + self.callsign
        if self.position is not None:
            s += ", " + str(self.position)

        return s

    def process_msg(self, ts, msg, refpos):
        self.msg_count += 1
        self.lastseen = ts
        if msg.is_adsb():
            if msg.has_callsign():
                self.callsign = msg.callsign
            elif msg.has_position():
                now = int(time.time())
                if self.tsmsg0 is None or (now - self.tsmsg0[0]) > 10 or msg.oe_flag() == self.tsmsg0[1].oe_flag():
                    self.tsmsg0 = (ts, msg)
                    self.tsmsg1 = None
                    self.position = None
                else:
                    self.tsmsg1 = self.tsmsg0
                    self.tsmsg0 = (ts, msg)
                    newpos = self.__calc_position(refpos)
                    if newpos is not None and newpos.distance_from(refpos) <= 463000: # 250 nm
                        self.position = newpos
                        return self.position
                    else:
                        self.tsmsg1 = None
                        self.position = None
        return None

    def __calc_position(self, refpos):
        if self.tsmsg0[1].oe_flag() == 0: # even
            even = self.tsmsg0
            odd = self.tsmsg1
        else:
            even = self.tsmsg1
            odd = self.tsmsg0
        try:
            pos = pyModeS.adsb.position(even[1].hex, odd[1].hex, even[0], odd[0], refpos.lat, refpos.lon)
        except:
            print("Erro determinando a posição, even = {}, odd = {}".format(even[1].hex, odd[1].hex))
            return None
        if pos is None:
            # msgs are in different latitude zones
            #see https://mode-s.org/api/_modules/pyModeS/decoder/bds/bds05.html#airborne_position
            return None
        else:
            return Position(*pos)
