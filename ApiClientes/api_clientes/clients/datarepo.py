import asyncio
from typing import Optional
from api_clientes.clients.client.get_users import get_users
from api_clientes.clients.client.models.usermodels import UserModel


class DataRepo:
    _instance = None

    _data: Optional[list[UserModel]] = None
    loaded = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataRepo, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.initialized = False
        self._data: Optional[list[UserModel]] = None

    def get_data(self) -> list[UserModel]:
        """
        Gets data from source or the cached version
        #TODO: Cache with redis for deployment

        Returns:
            List[UserModel]: The list of user models
        """
        if self._data is None and self.initialized is False:
            self.initialized = True
            print("Downloading new data")
            self._data = asyncio.run(get_users())
        else:
            print("Cached!")
        return self._data
