from regions.tags import Tag
from decimal import Decimal
from regions.definitions.regiontypes import RegionTypes


def test_get_tag():
    especial = (Decimal("-2.20"), Decimal("-40.276938"))
    tag = Tag.get_tag(especial[0], especial[1])
    assert tag == RegionTypes.ESPECIAL

    trabalhoso = (Decimal("-200.20"), Decimal("-400.276938"))
    tag = Tag.get_tag(trabalhoso[0], trabalhoso[1])
    assert tag == RegionTypes.TRABALHOSO
