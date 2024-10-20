from api_clientes.clients.client.expand_csv import expand_flattened_dict
from api_clientes.clients.client.models.usermodels import UserModel
import csv
from api_clientes.clients.client.get_users import validate_csv


def test_expand_csv():
    data = []

    with open(
        "api_clientes/clients/client/tests/mock/input-backend.csv", encoding="utf-8"
    ) as f:
        data_reader = csv.DictReader(f)
        for d in data_reader:
            expanded = expand_flattened_dict(d)
            data.append(expanded)

    validated = []
    for i, user in enumerate(data):
        validated.append(UserModel(**user))


def test_validate_csv():
    with open(
        "api_clientes/clients/client/tests/mock/input-backend.csv", encoding="utf-8"
    ) as f:
        data = f.read()
        validate_csv(data)
