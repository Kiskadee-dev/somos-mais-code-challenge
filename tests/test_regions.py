from regions.definitions.regiontypes import RegionTypes
from regions.regions import Regions


def test_regions():
    regs = Regions()
    assert len(regs.regions) > 0
    especial = regs.regions[RegionTypes.ESPECIAL]
    assert len(especial) > 1, "Especial has more than one region defined"
