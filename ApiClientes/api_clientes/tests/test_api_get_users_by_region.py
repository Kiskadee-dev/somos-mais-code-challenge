from django.urls import reverse
from rest_framework.test import APIClient


def test_get_by_region():
    client = APIClient()
    params = {"region": "sul"}
    url = reverse("users_by_region", kwargs=params)
    response = client.get(url, params)
    assert response.status_code != 500


def test_get_by_region_bad_params():
    client = APIClient()
    params = {"region": "old west"}
    url = reverse("users_by_region", kwargs=params)
    response = client.get(url, params)
    assert response.status_code == 400


def test_get_by_region_and_tag():
    client = APIClient()
    params = {"region": "sul", "tag": "normal"}
    url = reverse("users_by_region_and_tag", kwargs=params)
    response = client.get(url, params)
    assert response.status_code != 500
