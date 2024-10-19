from httpx import Response
import pytest
import respx
from rest_framework.test import APIClient
from django.urls import reverse

from api_clientes.clients.client.endpoints import EndpointRepo
from api_clientes.clients.client.tests.mock.load_mock_response import (
    get_mock_file_content,
)


@pytest.mark.skip("Implement pagination")
@respx.mock(assert_all_called=True)
def test_get_users(respx_mock):
    client = APIClient()
    url = reverse("users")
    respx_mock.get(EndpointRepo.users.value).mock(
        return_value=Response(status_code=200, content=get_mock_file_content())
    )
    response = client.get(url)

    content = response.json()
    assert response.status_code == 200
    assert "totalCount" in content
    assert "pageNumber" in content
    assert "pageSize" in content
    assert "users" in content
    assert len(content["users"]) > 0
