import os
from typing import Optional
from fakeredis import FakeRedis, FakeStrictRedis
import redis
from api_clientes.clients.datarepo import DataRepo


def get_redis_connection():
    return redis.StrictRedis(
        host=os.environ.get("REDIS_HOST", "redis"),
        port=os.environ.get("REDIS_PORT", 6379),
        db=os.environ.get("REDIS_DB", 0),
        decode_responses=True,
    )


redis_conn: Optional[FakeRedis | redis.StrictRedis] = None
if not os.environ.get("TESTING", True):
    redis_conn = get_redis_connection()
else:
    redis_conn = FakeStrictRedis()
DataRepo(redis_conn).get_data()
