from api_clientes.clients.datarepo import DataRepo


def test_datarepo_get(respx_fixture):
    data = DataRepo().get_data()
    assert type(data) is list
    assert len(data) > 0
