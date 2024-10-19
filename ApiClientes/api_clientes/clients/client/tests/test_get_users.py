from api_clientes.clients.client.get_users import get_users
from api_clientes.clients.client.tests.mock.load_mock_response import (
    get_mock_file_content,
)
import respx
from httpx import Response
from api_clientes.clients.client.endpoints import EndpointRepo


@respx.mock
# @pytest.mark.skip(reason="Must implement it along the user model")
def test_get_users():
    respx.get(EndpointRepo.users.value).mock(
        return_value=Response(status_code=200, content=get_mock_file_content())
    )
    result = get_users()
    assert len(result) > 0


@respx.mock
def test_gender_conversion():
    respx.get(EndpointRepo.users.value).mock(
        return_value=Response(status_code=200, content=get_mock_file_content())
    )
    result = get_users()
    for user in result:
        assert user.gender in ["M", "F", "O"]
