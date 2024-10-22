import os
from typing import Optional
from fakeredis import FakeStrictRedis
import redis
from api_clientes.clients.datarepo import DataRepo


def get_redis_connection():
    return redis.StrictRedis(
        host=os.environ.get("REDIS_HOST", "redis"),
        port=os.environ.get("REDIS_PORT", 6379),
        db=os.environ.get("REDIS_DB", 0),
        decode_responses=True,
    )


redis_conn: Optional[FakeStrictRedis | redis.StrictRedis] = None

TESTING = os.environ.get("TESTING", "True").lower() in ["true"]


if not TESTING:
    redis_conn = get_redis_connection()
    DataRepo(redis_conn).get_data()
else:
    print("Fake redis")
    redis_conn = FakeStrictRedis()
