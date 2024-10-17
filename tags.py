from enum import Enum
from decimal import Decimal
from math import sqrt, pow
from typing import Dict, List


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

    def has(self, x: Decimal, y: Decimal) -> bool:
        """Checks if a point is within this boundingbox

        Parameters
        ----------
        x : Decimal
        y : Decimal
        """
        return (self.x0 < x and self.y0 < y) and (self.x1 > x and self.y1 > y)

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
    class Countries(Enum):
        Brazil = 0

    class Tags(Enum):
        ESPECIAL = 0
        NORMAL = 1
        TRABALHOSO = 2

    Regions = {
        Countries.Brazil: {
            Tags.ESPECIAL: [
                BoundingBox(
                    Decimal("-2.196998"),
                    Decimal("-46.361899"),
                    Decimal("-15.411580"),
                    Decimal("-34.276938"),
                ),
                BoundingBox(
                    Decimal("-19.766959"),
                    Decimal("-52.997614"),
                    Decimal("-23.966413"),
                    Decimal("-44.428305"),
                ),
            ],
            Tags.NORMAL: BoundingBox(
                Decimal("-26.155681"),
                Decimal("-54.777426"),
                Decimal("-34.016466"),
                Decimal("-46.603598"),
            ),
            Tags.TRABALHOSO: BoundingBox(),
        }
    }


class Tag:

    def __init__(self, lat: Decimal, lon: Decimal):
        self.lat = lat
        self.lon = lon
