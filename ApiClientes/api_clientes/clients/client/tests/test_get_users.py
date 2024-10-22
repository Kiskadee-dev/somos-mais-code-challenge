from decimal import Decimal
import os

from pytest import raises
import api_clientes
from api_clientes.clients.client.exceptions import RequestFailed
from api_clientes.clients.client.models.usermodels import UserModel
import respx
from httpx import Response
from api_clientes.clients.client.endpoints import EndpointRepo
from api_clientes.clients.regions.definitions.regiontypes import RegionTypes
from api_clientes.clients.datarepo import DataRepo
from datetime import datetime


@respx.mock(assert_all_called=True)
def test_get_users_not_found(mocker, respx_mock, redis_client):
    respx_mock.get(EndpointRepo.users_json.value).mock(
        return_value=Response(status_code=404)
    )
    respx_mock.get(EndpointRepo.users_csv.value).mock(
        return_value=Response(status_code=404)
    )
    original_os_environ_get = os.environ.get

    def side_effect(*args, **kwargs):
        if args[0] == "TESTING_INIT_RETURNS_MOCKED_RESPONSES":
            return "False"
        return original_os_environ_get(*args, **kwargs)

    mocker.patch("os.environ.get", side_effect=side_effect)
    with raises(RequestFailed):
        DataRepo(api_clientes.redis_conn).get_data()


def test_get_users(respx_fixture, redis_client):
    result = DataRepo(api_clientes.redis_conn).get_data()
    assert len(result) == 2000


def test_gender_conversion(respx_fixture, redis_client):
    result = DataRepo(api_clientes.redis_conn).get_data()
    for user in result:
        assert user.gender in ["M", "F", "O"]


def test_user_region(respx_fixture, redis_client):
    result = DataRepo(api_clientes.redis_conn).get_data()

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


def test_user_attrs(respx_fixture, redis_client):
    result = DataRepo(api_clientes.redis_conn).get_data()
    for user in result:
        assert hasattr(user, "nationality")
        assert hasattr(user, "type")
        assert hasattr(user, "birthday")
        assert type(user.birthday) is datetime
        assert hasattr(user, "registered")
        assert type(user.registered) is datetime
        assert hasattr(user.location, "region")
