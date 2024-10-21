import os
import redis

from api_clientes.clients.datarepo import DataRepo


def get_redis_connection():
    return redis.StrictRedis(
        host=os.environ.get("REDIS_HOST", "localhost"),
        port=os.environ.get("REDIS_PORT", 6379),
        db=os.environ.get("REDIS_DB", 0),
        decode_responses=True,
    )


# You can call the function to create the connection
redis_conn = get_redis_connection()
DataRepo(redis_conn).get_data()
