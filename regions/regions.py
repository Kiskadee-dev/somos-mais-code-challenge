import re
from decimal import Decimal
from math import floor
from typing import Dict, List

from regions.boundingbox import BoundingBox
from regions.definitions.regiontypes import RegionTypes
from regions.definitions.values import VALUES


class Regions:
    def __init__(self) -> None:
        """Loads region files
        Each region has 2 coordinates composed by 4 values.
        If there are more than 4 and the file is still valid, the next 4 will be the same region.
        Due to a typo in the requirements file I'll use regex so its more generic than a simple split.
        """

        self.regions: Dict[RegionTypes, List[BoundingBox]] = {}
        pattern = r"(-?\d+.?\d+)"
        for key, definition in VALUES.items():
            if key not in self.regions:
                self.regions[key] = []

            matches = re.findall(pattern, definition)
            assert len(matches) % 4 == 0, f"Malformed region file: {key}"
            for i in range(floor(len(matches) / 4)):
                bounding = BoundingBox(
                    Decimal(
                        matches[0 * i],
                    ),
                    Decimal(matches[1 * i]),
                    Decimal(matches[2 * i]),
                    Decimal(matches[3 * i]),
                )
                self.regions[key].append(bounding)
