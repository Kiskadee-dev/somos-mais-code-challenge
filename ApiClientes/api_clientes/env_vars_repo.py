from enum import Enum


class EnvironVars(Enum):
    """Repo of all env vars used in this project

    Args:
        Enum (Str): The env var
    """

    REDIS_TESTING = "REDIS_TESTING"
    INIT = "INIT"
