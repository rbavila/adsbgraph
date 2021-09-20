from RRD import RRD

class MsgCountRRD(RRD):
    def __init__(self, rrdfile, grdir):
        super().__init__(rrdfile, grdir)

        data_items = {
            "modeac": ("Mode A/C", "#ff0000"),
            "df00": ("ACAS short", "#008000c0"),
            "df11": ("All-call", "#ff8000c0"),
            "df16": ("ACAS long", "#ffff00c0"),
            "df17": ("ADS-B", "#0040ffc0"),
            "other": ("Outras", "#ff00ffc0")
        }

        cdef_items = {
            "total": ("modeac,df00,+,df11,+,df16,+,df17,+,other,+", "Total", "#000000")
        }
        self.rra.extend([
            ("AVERAGE", 1),
            ("AVERAGE", 4),
            ("AVERAGE", 15),
            ("AVERAGE", 183)
        ])

        self.opts.update({
            "title": "Mensagens Mode S recebidas",
            "vertical-label": "msgs/s"
        })

        for di in data_items:
            self.ds[di] = ("DERIVE", 0, 1000)
            self.vdef[di + "avg"] = di + ",AVERAGE"
            self.vdef[di + "max"] = di + ",MAXIMUM"

        for (name, (rpn, title, color)) in cdef_items.items():
            self.cdef[name] = rpn
            self.vdef[name + "avg"] = name + ",AVERAGE"
            self.vdef[name + "max"] = name + ",MAXIMUM"

        self.gitems.append("COMMENT:{:13}{:>10}{:>10}\\n".format("", "Média", "Max"))

        i = 0
        for (di, (title, color)) in data_items.items():
            area = "AREA:{}{}:{}".format(di, color, "{:<10}".format(title))
            if i > 0:
                area += ":STACK"
            gavg = "GPRINT:{}avg:%8.2lf".format(di)
            gmax = "GPRINT:{}max:%8.2lf\\n".format(di)
            self.gitems.append(area)
            self.gitems.append(gavg)
            self.gitems.append(gmax)
            i += 1

        for (name, (rpn, title, color)) in cdef_items.items():
            line = "LINE0:{}{}:{}".format(name, color, "{:<10}".format(title))
            gavg = "GPRINT:{}avg:%8.2lf".format(name)
            gmax = "GPRINT:{}max:%8.2lf\\n".format(name)
            self.gitems.append(line)
            self.gitems.append(gavg)
            self.gitems.append(gmax)

if __name__ == "__main__":
    rrd = MsgCountRRD("teste.rrd", ".")
    if rrd.file_exists():
        print("Já existe")
    else:
        rrd.create()
