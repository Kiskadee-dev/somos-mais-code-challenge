import api_clientes
from api_clientes.clients.datarepo import DataRepo


def test_datarepo_get(respx_fixture, redis_client):
    data = DataRepo(api_clientes.redis_conn).get_data()
    assert type(data) is list
    assert len(data) > 0


def test_datarepo_get_cached(respx_fixture, redis_client):
    data = DataRepo(api_clientes.redis_conn).get_data()
    assert type(data) is list
    assert len(data) > 0
    data = DataRepo(api_clientes.redis_conn).get_data()
    assert type(data) is list
    assert len(data) > 0


def test_datarepo_wait(respx_fixture, redis_client):
    redis_client.flushall()
    redis_client.set(DataRepo.REDIS_LOCK_KEY, "True", nx=True, ex=10)
    DataRepo(api_clientes.redis_conn).get_data()
