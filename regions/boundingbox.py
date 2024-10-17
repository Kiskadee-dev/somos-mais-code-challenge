from decimal import Decimal
from math import pow, sqrt


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
        self.x0 = min(x0, x1)
        self.y0 = min(y0, y1)
        self.x1 = max(x0, x1)
        self.y1 = max(y0, y1)

    def has(self, x: Decimal, y: Decimal) -> bool:
        """Checks if a point is within this bounding box

        Parameters
        ----------
        x : Decimal
        y : Decimal
        """
        between_mins = self.x0 < x and self.y0 < y
        between_maxs = self.x1 > x and self.y1 > y
        return between_mins and between_maxs

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
