from api_clientes.utils.flatten_pydantic import flatten_pydantic
from pydantic import BaseModel


class Market(BaseModel):
    name: str
    location: str


class Somethin(BaseModel):
    bananas: int
    apples: int
    markets: list[Market]


def test_flattening():
    s = Somethin(
        bananas=10,
        apples=10,
        markets=[
            Market(name="SuperGeneric", location="Rua dos alfaces"),
            Market(name="SuperGeneric2", location="Rua dos alferes"),
        ],
    )
    flattened = flatten_pydantic(s)
    assert flattened["markets"][0]["name"] == "SuperGeneric"
    assert flattened["markets"][1]["name"] == "SuperGeneric2"
