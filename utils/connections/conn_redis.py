from redis import Redis

from project.settings import (
    REDIS_HOST,
    REDIS_PASSWORD,
    REDIS_PORT,
)

redis_db = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=0,
    password=REDIS_PASSWORD,
)
