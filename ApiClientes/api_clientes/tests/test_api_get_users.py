from rest_framework.test import APIClient
from django.urls import reverse
from api_clientes import redis_conn


def test_view_get_users(respx_fixture):
    redis_conn.flushall()
    client = APIClient()
    url = reverse("users")
    response = client.get(url)

    content = response.json()
    assert response.status_code == 200
    assert "totalCount" in content
    assert "pageNumber" in content
    assert "pageSize" in content
    assert "users" in content["results"]
    assert len(content["results"]["users"]) > 0

    # TODO: Fix pagination to include one ident
    # has_match = re.match(r"users: ", response.content.decode("utf-8"))
    # assert has_match is not None
