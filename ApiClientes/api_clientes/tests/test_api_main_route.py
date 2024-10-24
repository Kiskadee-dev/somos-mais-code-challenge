from django.urls import reverse
from rest_framework.test import APIClient


def test_main_routing(no_cache):
    client = APIClient()
    url = reverse("main")

    response = client.get(url)
    assert response.status_code == 200
    content = response.json()
    assert "results" in content
    results = content["results"]
    assert "endpoints" in results
    endpoints = results["endpoints"]
    for uri in endpoints:
        response = client.get(uri)
        assert response.status_code not in [404, 500]


def test_main_regions(no_cache):
    client = APIClient()
    url = reverse("regions")
    response = client.get(url)
    assert response.status_code == 200
    content = response.json()
    assert "results" in content


def test_main_tags(no_cache):
    client = APIClient()
    url = reverse("tags")

    response = client.get(url)
    assert response.status_code == 200
    content = response.json()
    assert "results" in content
