from decimal import Decimal


class Tag:

    def __init__(self, lat: Decimal, lon: Decimal):
        self.lat = lat
        self.lon = lon
