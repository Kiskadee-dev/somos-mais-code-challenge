from typing import Tuple
import asyncio
import json
import os
import time
from typing import Any, Optional
import uuid

from redis import Redis
from api_clientes.clients.client.get_users import get_users
from api_clientes.clients.client.models.usermodels import UserModel
from api_clientes.utils import flatten_pydantic
from api_clientes.env_vars_repo import EnvironVars
from datetime import datetime, timedelta


class DataRepo:
    _instance = None
    _cached_response: Optional[Tuple[list[UserModel], int]] = None

    _data: Optional[list[UserModel]] = None
    loaded = False
    APP_NAME = f"{__package__.rsplit('.', 1)[-1]}"
    REDIS_LOCK_KEY = f"{APP_NAME}:fetch_users_lock"
    REDIS_CACHE_KEY = f"{APP_NAME}:users"
    REDIS_USER_KEY = f"{REDIS_CACHE_KEY}:user"
    REDIS_REGION_KEY = f"{REDIS_CACHE_KEY}:region"

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DataRepo, cls).__new__(cls)
        return cls._instance

    def __init__(self, redis: Redis):
        self.redis = redis
        self.TESTING_INIT_RETURNS_MOCKED_RESPONSES = os.environ.get(
            EnvironVars.REDIS_TESTING.value, "True"
        ).lower() in ["true"]

    def none_or_val(self, value) -> Optional[Any]:
        """
        Fakeredis doesn't return none when get fails, so we convert

        Args:
            value: Any

        Returns:
            Optional[Any]: Value or None
        """
        copy = value
        if type(copy) is str:
            copy = copy.replace('"', "")
        return None if copy == "null" else value

    def save_in_memory(self, data):
        self._cached_response = (data, datetime.now() + timedelta(minutes=30))

    def get_data(self) -> list[UserModel]:
        """
        Gets data from source or the cached version

        Returns:
            List[UserModel]: The list of user models
        """
        if self._cached_response and self._cached_response[1] > datetime.now():
            return self._cached_response[0]
        self._cached_response = None

        users = []
        keys = []

        cursor = 0
        _, partial_keys = self.redis.scan(cursor, f"{self.REDIS_USER_KEY}*")

        if len(partial_keys) > 0:
            cursor = 0
            while True:
                cursor, partial_keys = self.redis.scan(
                    cursor, f"{self.REDIS_USER_KEY}*"
                )
                keys.extend(partial_keys)
                if cursor == 0:
                    break

        if len(keys) > 0:
            values = self.redis.mget(keys)
            print(f"Retrieved {len(values)} users from cache")
            response = [UserModel.model_validate_json(u) for u in values]
            self.save_in_memory(response)
            return response
        success = self.redis.set(self.REDIS_LOCK_KEY, "True", nx=True, ex=10)
        success = self.none_or_val(success)

        if not success:
            while self.redis.get(self.REDIS_LOCK_KEY):
                time.sleep(0.1)
            return self.get_data()

        print("Fetching new data.")

        users = asyncio.run(get_users(self.TESTING_INIT_RETURNS_MOCKED_RESPONSES))

        flattened_data = [
            flatten_pydantic.flatten_pydantic(u, by_alias=True) for u in users
        ]
        print("Saving cache data.")
        pipe = self.redis.pipeline()
        count = 0
        for user in flattened_data:
            dumped_data = json.dumps(user, default=str)
            user_id = str(uuid.uuid4())
            pipe.set(
                f"{self.REDIS_USER_KEY}:{user_id}",
                dumped_data,
            )
            pipe.sadd(
                f"{self.REDIS_REGION_KEY}:{user['location']['region']}",
                f"{self.REDIS_USER_KEY}:{user_id}",
            )
            count += 1
        pipe.execute()
        self.save_in_memory(users)
        print(f"Saved {count} users")

        self.redis.delete(self.REDIS_LOCK_KEY)
        return users
