from threading import Thread
from queue import SimpleQueue
from BEAST import BEAST
from ModeACMessage import ModeACMessage
from ModeSMessage import ModeSMessage
import time

class BEASTWorker(Thread):
    STATE_NOTSYNC = 0
    STATE_WAITSYNC = 1
    STATE_SYNC = 2

    def __init__(self, inbuf):
        super().__init__(name = "BEASTWorker", daemon = True)
        self.inbuf = inbuf
        self.msgqueue = SimpleQueue()
        self.state = self.STATE_NOTSYNC

    def run(self):
        while True:
            if self.state == self.STATE_NOTSYNC:
                print("OUT OF SYNC")
                b = self.inbuf.get()
                while b == BEAST.ESC:
                    b = self.inbuf.get()
                self.state = self.STATE_WAITSYNC

            if self.state == self.STATE_WAITSYNC:
                b = self.inbuf.get()
                while b != BEAST.ESC:
                    print("WAITING FOR SYNC")
                    b = self.inbuf.get()
                self.state = self.STATE_SYNC

            if self.state == self.STATE_SYNC:
                type = self.inbuf.get()

                mlat_ts = self.__receive_mlat_ts()
                if mlat_ts is None:
                    self.state = self.STATE_NOTSYNC
                    continue

                rssi = self.__receive_rssi()
                if rssi is None:
                    self.state = self.STATE_NOTSYNC
                    continue

                if type == BEAST.TYPE_MODEAC:
                    payload = self.__receive_unescaped(2)
                    if payload is None:
                        self.state = self.STATE_NOTSYNC
                        continue
                    ts = int(time.time())
                    m = ModeACMessage(payload)
                    self.msgqueue.put((ts, type, mlat_ts, rssi, m))
                elif type == BEAST.TYPE_MODESSHORT or type == BEAST.TYPE_MODESLONG:
                    if type == BEAST.TYPE_MODESSHORT:
                        payload = self.__receive_unescaped(7)
                    else:
                        payload = self.__receive_unescaped(14)
                    if payload is None:
                        self.state = self.STATE_NOTSYNC
                        continue
                    ts = int(time.time())
                    m = ModeSMessage(payload)
                    self.msgqueue.put((ts, type, mlat_ts, rssi, m))
                else:
                    self.state = self.STATE_NOTSYNC
                    continue

                self.state = self.STATE_WAITSYNC

    def __receive_mlat_ts(self):
        data = self.__receive_unescaped(6)
        if data is None:
            return None

        ts = 0
        for b in data:
            ts <<= 8
            ts += b
        return ts

    def __receive_rssi(self):
        data = self.__receive_unescaped(1)
        if data is None:
            return None

        rssi = data[0]
        return rssi

    def __receive_unescaped(self, n):
        data = bytearray(n)
        for i in range(n):
            b = self.inbuf.get()
            if b == BEAST.ESC:
                b = self.inbuf.get()
                if b != BEAST.ESC: # escaping error
                    return None
            data[i] = b
        return data
