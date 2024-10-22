from pydantic import BaseModel, ConfigDict
from api_clientes.clients.regions.definitions.locations import (
    BrazilRegions,
)
from api_clientes.clients.regions.definitions.regiontypes import RegionTypes


class QueryUserModel(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    region: BrazilRegions


class QueryUserByTagModel(QueryUserModel):
    tag: RegionTypes
