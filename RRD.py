import rrdtool
import os.path

class RRD:
    def __init__(self, rrdfile, grdir):
        self.rrdfile = rrdfile
        self.grdir = grdir
        self.opts = {
            "imgformat": "SVG",
            "width": 576,
            "height": 192
        }
        self.graphs = {
            "day": ("now - 48 hours", "HOUR:1:DAY:1:HOUR:4:0:%H:00"),
            "week": ("now - 8 days", "HOUR:6:DAY:1:DAY:1:0:%a"),
            "month": ("now - 30 days", "DAY:1:DAY:7:DAY:7:0:%d/%b"),
            "year": ("now - 366 days", "WEEK:1:MONTH:1:MONTH:1:0:%b")
        }
        self.ds = {} # name: (type, min, max)
        self.rra = [] # (type, steps)
        self.cdef = {} # name: rpn
        self.vdef = {} # name: rpn
        self.gitems = [] # expression

    def file_exists(self):
        return os.path.isfile(self.rrdfile)

    def create(self):
        params = ["--start", "now", "--step", "300"]

        for (name, (type, min, max)) in self.ds.items():
            p = "DS:{0}:{1}:600:{2}:{3}".format(name, type, min, max)
            params.append(p)

        for (type, steps) in self.rra:
            p = "RRA:{0}:0.5:{1}:576".format(type, steps)
            params.append(p)

        rrdtool.create(self.rrdfile, *params)

    def update(self, param):
        rrdtool.update(self.rrdfile, param)

    def graph(self):
        prefix = os.path.splitext(os.path.basename(self.rrdfile))[0]
        params = []
        for (k, v) in self.opts.items():
            params.append("--" + k)
            params.append(str(v))
        cf = self.rra[0][0]
        for (name, (type, min, max)) in self.ds.items():
            s = "DEF:{0}={1}:{0}:{2}".format(name, self.rrdfile, cf)
            params.append(s)
        for (name, rpn) in self.cdef.items():
            s = "CDEF:{0}={1}".format(name, rpn)
            params.append(s)
        for (name, rpn) in self.vdef.items():
            s = "VDEF:{0}={1}".format(name, rpn)
            params.append(s)
        params.extend(self.gitems)
        for (g, (t, xgrid)) in self.graphs.items():
            fname = "{}/{}_{}.svg".format(self.grdir, prefix, g)
            rrdtool.graph(fname,
                "--start", t,
                "--x-grid", xgrid,
                *params)

if __name__ == "__main__":
    rrd = RRD("teste.rrd", ".")
    rrd.graph()
