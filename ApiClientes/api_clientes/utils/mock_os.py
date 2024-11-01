import os

from api_clientes.env_vars_repo import EnvironVars


def allow_init(mocker):
    original_os_environ_get = os.environ.get

    def side_effect(*args, **kwargs):
        match args[0]:
            case EnvironVars.REDIS_TESTING.value:
                return "False"
            case EnvironVars.INIT.value:
                return "True"
            case _:
                return original_os_environ_get(*args, **kwargs)

    mocker.patch("os.environ.get", side_effect=side_effect)
