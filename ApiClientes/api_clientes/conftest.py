from httpx import Response
import pytest
import respx
import fakeredis


import api_clientes
from api_clientes.clients.client.endpoints import EndpointRepo
from api_clientes.clients.client.tests.mock.load_mock_response import (
    get_mock_file_content_csv,
    get_mock_file_content_json,
)
from api_clientes.utils import mock_os


@pytest.fixture(autouse=True)
def allow_init(mocker):
    mock_os.allow_init(mocker)


@pytest.fixture(scope="function")
def respx_fixture(mocker, allow_init):
    with respx.mock(assert_all_called=True) as respx_mock:
        mock_os.allow_init(mocker)

        respx_mock.get(EndpointRepo.users_json.value).mock(
            return_value=Response(status_code=200, content=get_mock_file_content_json())
        )
        respx_mock.get(EndpointRepo.users_csv.value).mock(
            return_value=Response(status_code=200, content=get_mock_file_content_csv())
        )
        yield respx_mock


@pytest.fixture(scope="function", autouse=True)
def redis_client(request, allow_init, mocker):
    fake_redis = fakeredis.FakeRedis()
    fake_redis.flushall()
    mocker.patch("api_clientes.redis_conn", new=fake_redis)
    mocker.patch("api_clientes.get_redis_connection", return_result=fake_redis)

    yield fake_redis
    fake_redis.flushall()


@pytest.fixture
def no_cache(scope="function"):
    if hasattr(api_clientes, "redis_conn"):
        api_clientes.redis_conn.flushall()
        return
    api_clientes.redis_conn = api_clientes.get_redis_connection()
