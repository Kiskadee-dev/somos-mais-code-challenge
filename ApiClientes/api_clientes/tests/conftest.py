import os
import pytest
import respx
from httpx import Response
from api_clientes.clients.client.endpoints import EndpointRepo
from api_clientes.clients.client.tests.mock.load_mock_response import (
    get_mock_file_content_csv,
    get_mock_file_content_json,
)


@pytest.fixture(scope="function")
def respx_fixture(mocker):
    with respx.mock(assert_all_called=True) as respx_mock:
        print("Patching respx")

        original_os_environ_get = os.environ.get

        def side_effect(*args, **kwargs):
            if args[0] == "TESTING_INIT_RETURNS_MOCKED_RESPONSES":
                return "False"
            return original_os_environ_get(*args, **kwargs)

        mocker.patch("os.environ.get", side_effect=side_effect)

        respx_mock.get(EndpointRepo.users_json.value).mock(
            return_value=Response(status_code=200, content=get_mock_file_content_json())
        )
        respx_mock.get(EndpointRepo.users_csv.value).mock(
            return_value=Response(status_code=200, content=get_mock_file_content_csv())
        )
        yield respx_mock
