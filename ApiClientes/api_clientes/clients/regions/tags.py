from decimal import Decimal
from api_clientes.clients.regions.definitions.regiontypes import (
    RegionTypes,
    Countries,
)
from api_clientes.clients.regions.regions import Regions
from api_clientes.clients.regions.boundingbox import BoundingBox
from typing import Tuple, Optional


class Tag:
    @staticmethod
    def get_tag(lon: Decimal, lat: Decimal, country=Countries.Brazil) -> RegionTypes:
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
        regions = Regions.get_instance().regions[country]

        default_tag = RegionTypes.TRABALHOSO
        smallest: Optional[Tuple[RegionTypes, BoundingBox]] = None
        for key, values in regions.items():
            boundaries = [boundary for boundary in values if boundary.has(x=lon, y=lat)]
            if len(boundaries) == 0:
                continue

            boundaries.sort(key=lambda x: x.size())
            if smallest is None or boundaries[0].size() < smallest[1].size():
                smallest = (key, boundaries[0])

        return default_tag if smallest is None else smallest[0]
