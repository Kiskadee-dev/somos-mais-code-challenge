import asyncio
import json
import time
from typing import Any, Optional

from redis import Redis
from api_clientes.clients.client.get_users import get_users
from api_clientes.clients.client.models.usermodels import UserModel
from api_clientes.utils import flatten_pydantic


class DataRepo:
    _instance = None

    _data: Optional[list[UserModel]] = None
    loaded = False

    REDIS_LOCK_KEY = f"{__package__.rsplit('.', 1)[-1]}:fetch_users_lock"
    REDIS_CACHE_KEY = f"{__package__.rsplit('.', 1)[-1]}:users"

    def __init__(self, redis: Redis):
        self.redis = redis

    def none_or_val(self, value) -> Optional[Any]:
        """Fakeredis doesn't return none when get fails, so we convert

        Args:
            value: Any

        Returns:
            Optional[Any]: Value or None
        """
        copy = value
        if type(copy) is str:
            copy = copy.replace('"', "")
        return None if copy == "null" else value

    def get_data(self) -> list[UserModel]:
        """
        Gets data from source or the cached version

        Returns:
            List[UserModel]: The list of user models
        """

        data = self.redis.get(self.REDIS_CACHE_KEY)
        data = self.none_or_val(data)

        if data:
            data = json.loads(data)
            return [UserModel(**u) for u in data]

        success = self.redis.set(self.REDIS_LOCK_KEY, "True", nx=True, ex=5)
        success = self.none_or_val(success)

        if not success:
            while self.redis.get(self.REDIS_LOCK_KEY):
                time.sleep(0.1)
            return self.get_data()

        print("Fetching new data.")
        users = asyncio.run(get_users())
        flattened_data = [
            flatten_pydantic.flatten_pydantic(u, by_alias=True) for u in users
        ]
        print("Saving cache data.")
        self.redis.set(self.REDIS_CACHE_KEY, json.dumps(flattened_data, default=str))
        self.redis.delete(self.REDIS_LOCK_KEY)
        return users
