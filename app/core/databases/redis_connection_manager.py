import redis.asyncio as redis

from app.core.databases.base_connection_manager import BaseConnectionManager


class RedisConnectionManager(BaseConnectionManager):
    def _get_name(self):
        return "redis"

    async def connect(self):
        if self.pool is None:
            self.pool = redis.ConnectionPool.from_url(
                self.uri,
                max_connections=self.max_pool_size,
                decode_responses=True
            )
            self.client = redis.Redis(connection_pool=self.pool)
        return self.client

    async def close(self):
        if self.client:
            await self.client.close()
            self.pool = None
            self.client = None

    async def get(self, key):
        if not self.client:
            await self.connect()
        return await self.client.get(key)

    async def set(self, key, value, ex=None):
        if not self.client:
            await self.connect()
        return await self.client.set(key, value, ex=ex)

    async def delete(self, *keys):
        if not self.client:
            await self.connect()
        return await self.client.delete(*keys)

    async def exists(self, *keys):
        if not self.client:
            await self.connect()
        return await self.client.exists(*keys)

    async def publish(self, channel, message):
        if not self.client:
            await self.connect()
        return await self.client.publish(channel, message)