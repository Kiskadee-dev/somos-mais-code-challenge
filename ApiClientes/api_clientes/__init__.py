import os
from typing import Optional
from fakeredis import FakeStrictRedis
import redis
from api_clientes.clients.datarepo import DataRepo


INIT = os.environ.get("INIT", "False").lower() in ["true"]
REDIS_TESTING = os.environ.get("TESTING", "True").lower() in ["true"]


def get_redis_connection() -> redis.StrictRedis | FakeStrictRedis:
    return (
        redis.StrictRedis(
            host=os.environ.get("REDIS_HOST", "redis"),
            port=os.environ.get("REDIS_PORT", 6379),
            db=os.environ.get("REDIS_DB", 0),
            decode_responses=True,
        )
        if not REDIS_TESTING
        else FakeStrictRedis()
    )


redis_conn: Optional[FakeStrictRedis | redis.StrictRedis] = None


def load_data():
    DataRepo(redis_conn).get_data()


if INIT:
    redis_conn = get_redis_connection()
