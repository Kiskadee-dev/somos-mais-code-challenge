from enum import Enum
from decimal import Decimal
from math import sqrt, pow


class BoundingBox:

    def __init__(self, x0: Decimal, y0: Decimal, x1: Decimal, y1: Decimal) -> None:
        """This class accepts 2 points in space to form a boundary

        Parameters
        ----------
        x0 : Decimal
        y0 : Decimal
        x1 : Decimal
        y1 : Decimal
        """
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

    def has(self, x: Decimal, y: Decimal):
        pass

    def size(self) -> float:
        """Returns the size of the bounding box

        Returns
        -------
        float
            The size
        """
        p0 = (self.x0, self.y0)
        p1 = (self.x1, self.y0)
        p2 = (self.x0, self.y1)
        p3 = (self.x1, self.y1)

        d0 = sqrt(pow((p1[0] - p0[0]), 2) + pow((p1[1] - p0[1]), 2))
        d1 = sqrt(pow((p3[0] - p2[0]), 2) + pow((p3[1] - p2[1]), 2))
        return abs(d0) * abs(d1)


class Coordinates:

    class Brazil(Enum):
        pass


class Tag:

    def __init__(self, lat: Decimal, lon: Decimal):
        self.lat = lat
        self.lon = lon
