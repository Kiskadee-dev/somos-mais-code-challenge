from api_clientes.clients.client.endpoints import EndpointRepo
from api_clientes.clients.client.exceptions import RequestFailed
from api_clientes.clients.client.models.usermodels import UserModel
import httpx
import asyncio
import csv
from io import StringIO


async def validate(data: dict) -> list[UserModel]:
    validated_data = [UserModel.model_validate(user) for user in data]
    return validated_data


async def validate_csv(data: str) -> list[UserModel]:
    csv_file = StringIO(data)
    reader = csv.DictReader(csv_file)
    validated_data = [UserModel.model_validate(user) for user in reader]
    return validated_data


async def get_users() -> list[UserModel]:
    """Get users and validate

    Raises:
        Exception:
        RequestFailed
    """
    async with httpx.AsyncClient() as client:
        response_1_coro = client.get(EndpointRepo.users_json.value)
        response_2_coro = client.get(EndpointRepo.users_csv.value)

        response_1, response_2 = await asyncio.gather(response_1_coro, response_2_coro)

        for response in [response_1, response_2]:
            if response.status_code != 200:
                raise RequestFailed(
                    f"{response.status_code}, {response.url},\n{response.content}"
                )

        json_data = response_1.json()
        validated_data = await asyncio.gather(
            validate(json_data["results"]),
            # validate_csv(response_2.content.decode("utf-8").lstrip("\ufeff")),
        )

        # TODO: Merge json with csv
        return validated_data[0]
