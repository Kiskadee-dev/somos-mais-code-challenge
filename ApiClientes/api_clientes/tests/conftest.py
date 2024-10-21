import pytest
import respx
from httpx import Response
from api_clientes.clients.client.endpoints import EndpointRepo
from api_clientes.clients.client.tests.mock.load_mock_response import (
    get_mock_file_content_csv,
    get_mock_file_content_json,
)


@pytest.fixture()
def respx_fixture():
    with respx.mock(assert_all_called=True) as respx_mock:
        print("Patching respx")
        respx_mock.get(EndpointRepo.users_json.value).mock(
            return_value=Response(status_code=200, content=get_mock_file_content_json())
        )
        respx_mock.get(EndpointRepo.users_csv.value).mock(
            return_value=Response(status_code=200, content=get_mock_file_content_csv())
        )
        yield respx_mock
