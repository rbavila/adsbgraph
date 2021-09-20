from threading import Thread
from BEAST import BEAST
from ModeSMessage import ModeSMessage
from Aircraft import Aircraft
from Position import Position
from RangeRegister import RangeRegister

class DataWorker(Thread):
    def __init__(self, msgqueue):
        super().__init__(name = "DataWorker", daemon = True)
        self.msgqueue = msgqueue
        self.stats = {
            "messageCount": {
                "modeAC": 0,
                "modeS": {
                    0: 0,
                    11: 0,
                    16: 0,
                    17: 0,
                    "other": 0
                }
            }
        }
        self.aircrafts = {}
        self.home = Position(-30.028, -51.191)
        self.rr = RangeRegister()

    def run(self):
        # dump = open("dump.txt", "w")
        while True:
            (ts, type, mlat_ts, rssi, m) = self.msgqueue.get()
            if type == BEAST.TYPE_MODEAC:
                self.stats["messageCount"]["modeAC"] += 1
            elif m.df == 0 or m.df == 11 or m.df == 16 or m.df == 17:
                self.stats["messageCount"]["modeS"][m.df] += 1
            else:
                self.stats["messageCount"]["modeS"]["other"] += 1

            if type != BEAST.TYPE_MODEAC and m.icao is not None:
                # dump.write("{}\t{}\n".format(ts, m.hex))
                # dump.flush()
                if m.icao not in self.aircrafts:
                    self.aircrafts[m.icao] = Aircraft(m.icao)
                a = self.aircrafts[m.icao]
                pos = a.process_msg(ts, m, self.home)
                if pos is not None:
                    nmdist = pos.distance_from(self.home) / 1852
                    quad = self.__quadrant(pos)
                    # print("[dw] rr update: {} {}".format(quad, nmdist))
                    self.rr.update(quad, nmdist)

    def __quadrant(self, pos):
        dlat = pos.lat - self.home.lat
        dlon = pos.lon - self.home.lon
        q = "n" if dlat > 0 else "s"
        q += "w" if dlon < 0 else "e"
        return q
