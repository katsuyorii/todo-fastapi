from redis.asyncio import Redis

from typing import Any


class RedisBaseRepository:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client
    
    async def get(self, key: str) -> Any:
        return await self.redis.get(key)

    async def set(self, key: str, value: Any) -> None:
        await self.redis.set(key, value)
    
    async def setex(self, key: str, value: Any, expire: int) -> None:
        await self.redis.set(key, value, expire)

    async def delete(self, key: str) -> None:
        await self.redis.delete(key)
    
    async def exists(self, key: str) -> bool:
        return bool(await self.redis.exists(key))