from decimal import Decimal
from api_clientes.clients.client.get_users import get_users
from api_clientes.clients.client.models.usermodels import UserModel
from api_clientes.clients.client.tests.mock.load_mock_response import (
    get_mock_file_content,
)
import respx
from httpx import Response
from api_clientes.clients.client.endpoints import EndpointRepo
from api_clientes.clients.regions.definitions.regiontypes import RegionTypes


@respx.mock(assert_all_called=True)
# @pytest.mark.skip(reason="Must implement it along the user model")
def test_get_users(respx_mock):
    respx_mock.get(EndpointRepo.users.value).mock(
        return_value=Response(status_code=200, content=get_mock_file_content())
    )
    result = get_users()
    assert len(result) > 0


@respx.mock(assert_all_called=True)
def test_gender_conversion(respx_mock):
    respx_mock.get(EndpointRepo.users.value).mock(
        return_value=Response(status_code=200, content=get_mock_file_content())
    )
    result = get_users()
    for user in result:
        assert user.gender in ["M", "F", "O"]


@respx.mock(assert_all_called=True)
def test_user_region(respx_mock):
    respx_mock.get(EndpointRepo.users.value).mock(
        return_value=Response(status_code=200, content=get_mock_file_content())
    )
    result = get_users()

    user_by_type: dict[str, list[UserModel]] = {}
    for user in result:
        assert user.type is not None
        assert RegionTypes(user.type)
        if user.type not in user_by_type:
            user_by_type[user.type] = []
        user_by_type[user.type].append(user)

    assert RegionTypes.ESPECIAL.value in user_by_type
    assert RegionTypes.NORMAL.value in user_by_type
    assert RegionTypes.TRABALHOSO.value in user_by_type

    assert len(user_by_type[RegionTypes.ESPECIAL.value]) > 0
    assert len(user_by_type[RegionTypes.NORMAL.value]) > 0
    assert len(user_by_type[RegionTypes.TRABALHOSO.value]) > 0

    u = next(iter(result))

    especial = (Decimal("-2.20"), Decimal("-40.276938"))
    trabalhoso = (Decimal("-200.20"), Decimal("-400.276938"))

    u.location.coordinates.longitude, u.location.coordinates.latitude = especial
    assert RegionTypes(u.type) == RegionTypes.ESPECIAL

    u.location.coordinates.longitude, u.location.coordinates.latitude = trabalhoso
    assert RegionTypes(u.type) == RegionTypes.TRABALHOSO
