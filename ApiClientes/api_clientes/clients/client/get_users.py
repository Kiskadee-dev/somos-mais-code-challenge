from ApiClientes.api_clientes.clients.client.endpoints import EndpointRepo
from ApiClientes.api_clientes.clients.client.exceptions import RequestFailed
from ApiClientes.api_clientes.clients.client.models.usermodels import UserModel
import httpx


async def get_users() -> list[UserModel]:
    """Get users and validate

    Raises:
        Exception:
        RequestFailed
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(EndpointRepo.users.value)
        if response.status_code != 200:
            raise RequestFailed(f"{response.status_code}, {response.content}")
        data = response.json()
        return [UserModel.model_validate(user) for user in data["results"]]
