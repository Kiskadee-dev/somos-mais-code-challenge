from api_clientes.clients.client.endpoints import EndpointRepo
from api_clientes.clients.client.exceptions import RequestFailed
from api_clientes.clients.client.models.usermodels import UserModel
import httpx


def get_users() -> list[UserModel]:
    """Get users and validate

    Raises:
        Exception:
        RequestFailed
    """
    response = httpx.get(EndpointRepo.users.value)
    if response.status_code != 200:
        raise RequestFailed(f"{response.status_code}, {response.content}")
    data = response.json()
    return [UserModel.model_validate(user) for user in data["results"]]
