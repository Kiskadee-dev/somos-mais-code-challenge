from decimal import Decimal
from regions.definitions.regiontypes import RegionTypes


class Tag:
    @staticmethod
    def find_tag(lat: Decimal, lon: Decimal) -> RegionTypes:
        """Given a point in space, determine which boundary contains it and return
        the appropriate tag.

        The requirements vaguely mentions about future system expansion, so we account for 2 edge cases.
        1. Boundaries that contains another boundary
        2. Boundary intersections

        In both cases, the smaller or more specific boundary takes precedence, so we'll return the tag of the most specific boundary.

        Args:
            lat (Decimal)
            lon (Decimal)

        Returns:
            RegionTypes: The tag
        """
        raise NotImplementedError()
