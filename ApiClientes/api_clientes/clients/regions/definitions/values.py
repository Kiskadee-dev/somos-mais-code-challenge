from ApiClientes.api_clientes.clients.regions.definitions.regiontypes import (
    RegionTypes,
    Countries,
)

VALUES = {
    Countries.Brazil: {
        RegionTypes.ESPECIAL: """
            minlon: -2.196998
            minlat -46.361899
            maxlon: -15.411580
            maxlat: -34.276938

            minlon: -19.766959
            minlat -52.997614
            maxlon: -23.966413
            maxlat: -44.428305
        """,
        RegionTypes.NORMAL: """
            minlon: -26.155681
            minlat -54.777426
            maxlon: -34.016466
            maxlat: -46.603598
        """,
    }
}
