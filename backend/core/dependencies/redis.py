from fastapi import Depends

from redis.asyncio import Redis

from src.redis import redis_client
from core.repositories.redis_base import RedisBaseRepository


async def get_redis() -> Redis:
    return redis_client

def get_redis_repository(redis_client: Redis = Depends(get_redis)) -> RedisBaseRepository:
    return RedisBaseRepository(redis_client)