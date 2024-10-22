from api_clientes.clients.regions.definitions.locations import (
    brazil_regions,
    BrazilRegions,
    find_region,
)


def test_amount():
    assert len(brazil_regions) == 5
    amount = 0
    for k, v in brazil_regions.items():
        for i in v:
            amount += 1
    assert amount == 27


def test_lookup():
    state = "Rio de Janeiro"
    has_match = find_region(state)
    assert has_match == BrazilRegions.SUDESTE

    state = "Wakanda"
    has_match = find_region(state)
    assert has_match is None
