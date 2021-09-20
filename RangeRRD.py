from RRD import RRD

class RangeRRD(RRD):
    def __init__(self, rrdfile, grdir):
        super().__init__(rrdfile, grdir)

        data_items = {
            "nw": ("NW", "#ff0000a0"),
            "ne": ("NE", "#00a000a0"),
            "se": ("SE", "#ffa000a0"),
            "sw": ("SW", "#0000ffa0")
        }

        self.rra.extend([
            ("MAX", 1),
            ("MAX", 4),
            ("MAX", 15),
            ("MAX", 183)
        ])

        self.vdef.update({
            "nwmax": "nw,MAXIMUM",
            "nemax": "ne,MAXIMUM",
            "semax": "se,MAXIMUM",
            "swmax": "sw,MAXIMUM"
        })

        self.opts.update({
            "title": "Range máximo",
            "vertical-label": "NM",
            "y-grid": "10:1",
#            "units-length": "4"
        })

        for di in data_items:
            self.ds[di] = ("GAUGE", 0, 263)

        self.cdef["swneg"] = "sw,-1,*"
        self.cdef["seneg"] = "se,-1,*"

        self.gitems.append("LINE1:{0}{2}:{1}\\g".format("nw", *data_items["nw"]))
        self.gitems.append("GPRINT:nwmax:%7.2lf  ")
        self.gitems.append("LINE1:{0}{2}:{1}\\g".format("ne", *data_items["ne"]))
        self.gitems.append("GPRINT:nemax:%7.2lf  ")
        # self.gitems.append("COMMENT:\\n")
        self.gitems.append("LINE1:{0}{2}:{1}\\g".format("swneg", *data_items["sw"]))
        self.gitems.append("GPRINT:swmax:%7.2lf  ")
        self.gitems.append("LINE1:{0}{2}:{1}\\g".format("seneg", *data_items["se"]))
        self.gitems.append("GPRINT:semax:%7.2lf\\c")

if __name__ == "__main__":
    rrd = RangeRRD("teste_range.rrd", ".")
    if not rrd.file_exists():
        rrd.create()
    rrd.graph()
