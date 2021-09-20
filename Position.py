import math

class Position:
    R = 6371000 # raio médio da Terra em metros

    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
        self.rlat = lat * math.pi / 180
        self.rlon = lon * math.pi / 180
        self.cos_rlat = math.cos(self.rlat)

    def __str__(self):
        return "[{}, {}]".format(self.lat, self.lon)

    def distance_from(self, pos):
        # https://www.movable-type.co.uk/scripts/latlong.html
        dlat = self.rlat - pos.rlat
        dlon = self.rlon - pos.rlon
        sin_dlat2 = math.sin(dlat / 2)
        sin_dlon2 = math.sin(dlon / 2)
        a = (sin_dlat2 * sin_dlat2 +
            pos.cos_rlat * self.cos_rlat * sin_dlon2 * sin_dlon2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = Position.R * c
        return d

if __name__ == "__main__":
    home = Position(-30.028, -51.191)
    p = Position(-29.19627, -51.18859)
    print(home, p)
    print(p.distance_from(home))
