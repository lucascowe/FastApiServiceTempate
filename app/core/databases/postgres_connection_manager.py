import asyncpg

from app.core.databases.base_connection_manager import BaseConnectionManager


class PostgresConnectionManager(BaseConnectionManager):
    def _get_name(self):
        return "postgresql"

    async def connect(self):
        if self.pool is None:
            self.pool = await asyncpg.create_pool(
                dsn=self.uri,
                min_size=self.min_pool_size,
                max_size=self.max_pool_size,
                max_inactive_connection_lifetime=self.idle_timeout,
            )
        return self.pool

    async def close(self):
        if self.pool:
            await self.pool.close()
            self.pool = None

    async def get_connection(self):
        if not self.pool:
            await self.connect()
        return await self.pool.acquire()

    async def release_connection(self, connection):
        await self.pool.release(connection)

    async def execute(self, query, *args):
        async with self.pool.acquire() as connection:
            return await connection.execute(query, *args)

    async def fetch(self, query, *args):
        async with self.pool.acquire() as connection:
            return await connection.fetch(query, *args)

    async def fetchval(self, query, *args):
        async with self.pool.acquire() as connection:
            return await connection.fetchval(query, *args)