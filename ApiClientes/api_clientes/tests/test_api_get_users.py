import re
import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from api_clientes import redis_conn


@pytest.fixture(scope="function", autouse=True)
def no_cache():
    redis_conn.flushall()


def test_view_get_users(respx_fixture, no_cache):
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


def test_view_get__users_pagination_ident(respx_fixture, no_cache):
    client = APIClient()
    url = reverse("users")
    response = client.get(url)
    data = response.content.decode("utf-8")
    has_match = re.search(r'"users": ', data)
    assert has_match is not None


def test_view_get_users_pagination(respx_fixture, no_cache):
    client = APIClient()
    url = reverse("users")
    response = client.get(f"{url}?pageNumber=8")

    content = response.json()
    assert response.status_code == 200
    assert "pageNumber" in content
    assert content["pageNumber"] == 8


def test_view_get_users_pagination_size(respx_fixture, no_cache):
    client = APIClient()
    url = reverse("users")
    response = client.get(f"{url}?pageSize=8")

    content = response.json()
    assert response.status_code == 200
    assert "pageSize" in content
    assert "users" in content["results"]
    assert len(content["results"]["users"]) == 8
    assert content["pageSize"] == 8
