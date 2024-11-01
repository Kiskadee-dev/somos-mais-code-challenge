from django.urls import reverse
from rest_framework.test import APIClient

from api_clientes.clients.datarepo import DataRepo


def test_get_by_region(respx_fixture, redis_client):
    DataRepo(redis_client).get_data()
    client = APIClient()
    params = {"region": "sul"}
    url = reverse("users_by_region", kwargs=params)
    response = client.get(url, params)
    assert response.status_code == 200
    content = response.json()
    assert "totalCount" in content
    assert "pageNumber" in content
    assert "pageSize" in content
    assert "results" in content
    assert "users" in content["results"]
    assert len(content["results"]["users"]) > 0


def test_get_by_region_bad_params(respx_fixture, redis_client):
    DataRepo(redis_client).get_data()
    client = APIClient()
    params = {"region": "old-west"}
    url = reverse("users_by_region", kwargs=params)
    response = client.get(url, params)
    assert response.status_code == 400
    content = response.json()
    assert "errors" in content


def test_get_by_region_and_tag(respx_fixture, redis_client):
    DataRepo(redis_client).get_data()
    client = APIClient()
    params = {"region": "sul", "tag": "normal"}
    url = reverse("users_by_region_and_tag", kwargs=params)
    response = client.get(url, params)
    assert response.status_code == 200
    content = response.json()
    assert "totalCount" in content
    assert "pageNumber" in content
    assert "pageSize" in content
    assert "results" in content
    assert "users" in content["results"]
    assert len(content["results"]["users"]) > 0
