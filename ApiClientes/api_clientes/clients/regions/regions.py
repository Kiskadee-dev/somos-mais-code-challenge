import re
from decimal import Decimal
from math import floor
from typing import Dict, List

from api_clientes.clients.regions.boundingbox import BoundingBox
from api_clientes.clients.regions.definitions.regiontypes import (
    RegionTypes,
    Countries,
)
from api_clientes.clients.regions.definitions.values import VALUES


class Regions:
    _instance = None

    def __init__(self) -> None:
        """Repository that loads region files
        Each region has 2 coordinates composed by 4 values.
        If there are more than 4 and the file is still valid, the next 4 will be the same region.
        Due to a typo in the requirements file I'll use regex so its more generic than a simple split.
        """

        self.regions: Dict[Countries, Dict[RegionTypes, List[BoundingBox]]] = {}
        pattern = r"(-?\d+.?\d+)"
        for country, country_regions in VALUES.items():
            if country not in self.regions:
                self.regions[country] = {}

            for key, definition in country_regions.items():
                if key not in self.regions[country]:
                    self.regions[country][key] = []

                matches = re.findall(pattern, definition)
                assert len(matches) % 4 == 0, f"Malformed region file: {key}"

                for i in range(floor(len(matches) / 4)):
                    bounding = BoundingBox(
                        Decimal(
                            matches[0 + (i * 4)],
                        ),
                        Decimal(matches[1 + (i * 4)]),
                        Decimal(matches[2 + (i * 4)]),
                        Decimal(matches[3 + (i * 4)]),
                    )
                    self.regions[country][key].append(bounding)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
