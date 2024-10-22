from enum import Enum
from typing import Optional


class BrazilRegions(Enum):
    NORTE = "norte"
    NORDESTE = "nordeste"
    CENTRO_OESTE = "centro-oeste"
    SUDESTE = "sudeste"
    SUL = "sul"


brazil_regions = {
    BrazilRegions.NORTE: [
        "acre",
        "amapá",
        "amazonas",
        "pará",
        "rondônia",
        "roraima",
        "tocantins",
    ],
    BrazilRegions.NORDESTE: [
        "alagoas",
        "bahia",
        "ceará",
        "maranhão",
        "paraíba",
        "pernambuco",
        "piauí",
        "rio grande do norte",
        "sergipe",
    ],
    BrazilRegions.CENTRO_OESTE: [
        "distrito federal",
        "goiás",
        "mato grosso",
        "mato grosso do sul",
    ],
    BrazilRegions.SUDESTE: [
        "espírito santo",
        "minas gerais",
        "rio de janeiro",
        "são paulo",
    ],
    BrazilRegions.SUL: ["paraná", "rio grande do sul", "santa catarina"],
}


def find_region(state: str) -> Optional[BrazilRegions]:
    state = state.lower()
    for k, v in brazil_regions.items():
        if state in v:
            return k
    return None
