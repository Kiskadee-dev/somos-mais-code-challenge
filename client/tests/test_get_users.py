import pytest
from client.get_users import get_users
from client.tests.mock.load_mock_response import get_mock_file_content
import respx
from httpx import Response
from client.endpoints import EndpointRepo


@pytest.mark.asyncio
@respx.mock
# @pytest.mark.skip(reason="Must implement it along the user model")
async def test_get_users():
    respx.get(EndpointRepo.users.value).mock(
        return_value=Response(status_code=200, content=get_mock_file_content())
    )
    result = await get_users()
    assert len(result) > 0
