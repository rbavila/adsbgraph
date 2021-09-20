from threading import Thread
from threading import Lock
from MsgCountRRD import MsgCountRRD
from RangeRRD import RangeRRD
from time import sleep
from time import time

class RRDWorker(Thread):
    def __init__(self, stats, rr, m_rrdfile, r_rrdfile, grdir):
        super().__init__(name = "RRDWorker", daemon = True)
        self.update_lock = Lock()
        self.stats = stats
        self.rr = rr
        self.msgcountrrd = MsgCountRRD(m_rrdfile, grdir)
        if not self.msgcountrrd.file_exists():
            self.msgcountrrd.create()
        self.rangerrd = RangeRRD(r_rrdfile, grdir)
        if not self.rangerrd.file_exists():
            self.rangerrd.create()

    def run(self):
        now = int(time())
        t = ((now + 300) // 300) * 300 - now + 1
        sleep(t)
        while True:
            aligned_now = (int(time()) // 300) * 300
            m_param = "{}:{}:{}:{}:{}:{}:{}".format(
                aligned_now,
                self.stats["messageCount"]["modeAC"],
                self.stats["messageCount"]["modeS"][0],
                self.stats["messageCount"]["modeS"][11],
                self.stats["messageCount"]["modeS"][16],
                self.stats["messageCount"]["modeS"][17],
                self.stats["messageCount"]["modeS"]["other"]
            )
            ranges = self.rr.resetget()
            r_param = "{}:{}:{}:{}:{}".format(aligned_now, *ranges)
            with self.update_lock:
                self.msgcountrrd.update(m_param)
                self.rangerrd.update(r_param)
                self.msgcountrrd.graph()
                self.rangerrd.graph()
            now = int(time())
            t = ((now + 300) // 300) * 300 - now + 1
            sleep(t)
