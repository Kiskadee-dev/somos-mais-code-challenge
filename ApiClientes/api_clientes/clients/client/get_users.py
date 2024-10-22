from api_clientes.clients.client.endpoints import EndpointRepo
from api_clientes.clients.client.exceptions import RequestFailed
from api_clientes.clients.client.models.usermodels import UserModel
import httpx
import asyncio
import csv
from io import StringIO
from api_clientes.clients.client.expand_csv import expand_flattened_dict
from api_clientes.clients.client.tests.mock.load_mock_response import (
    get_mock_file_content_csv,
    get_mock_file_content_json,
)


def validate(data: dict) -> list[UserModel]:
    validated_data = [UserModel.model_validate(user) for user in data]
    return validated_data


def validate_csv(data: str) -> list[UserModel]:
    csv_file = StringIO(data)
    reader = csv.DictReader(csv_file)
    expanded = (expand_flattened_dict(flattened) for flattened in reader)
    validated_data = [UserModel.model_validate(user) for user in expanded]
    return validated_data


async def get_users(mocked=False) -> list[UserModel]:
    """Get users and validate

    Raises:
        Exception:
        RequestFailed
    """
    async with httpx.AsyncClient() as client:
        if mocked:
            response_1, response_2 = (
                httpx.Response(status_code=200, content=get_mock_file_content_json()),
                httpx.Response(status_code=200, content=get_mock_file_content_csv()),
            )
        else:
            response_1_coro = client.get(EndpointRepo.users_json.value)
            response_2_coro = client.get(EndpointRepo.users_csv.value)

            response_1, response_2 = await asyncio.gather(
                response_1_coro, response_2_coro
            )

        for response in [response_1, response_2]:
            if response.status_code != 200:
                raise RequestFailed(
                    f"{response.status_code}, {response.url},\n{response.content}"
                )

        json_data = response_1.json()
        validated_json_data, validated_csv_data = (
            validate(json_data["results"]),
            validate_csv(response_2.content.decode("utf-8")),
        )

        return validated_json_data + validated_csv_data
