from regions.definitions.regiontypes import RegionTypes, Countries
from regions.regions import Regions


def test_regions():
    regs = Regions()
    assert len(regs.regions) > 0
    assert Countries.Brazil in regs.regions
    especial = regs.regions[Countries.Brazil][RegionTypes.ESPECIAL]
    assert len(especial) > 1, "Especial has more than one region defined"
