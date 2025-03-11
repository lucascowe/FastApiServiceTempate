import motor.motor_asyncio
from app.core.databases.base_connection_manager import BaseConnectionManager


class MongoConnectionManager(BaseConnectionManager):
    def _get_name(self):
        return "mongodb"

    def _build_uri(self):
        auth_part = f"{self._user}:{self._password}@" if self._user and self._password else ""
        return f"mongodb://{auth_part}{self.host}:{self.port}/{self.db_name}"

    async def connect(self):
        if self.pool is None:
            # Motor doesn't use a traditional connection pool like asyncpg
            # but it does manage connections internally
            client = motor.motor_asyncio.AsyncIOMotorClient(
                self.uri,
                maxPoolSize=self.max_pool_size,
                minPoolSize=self.min_pool_size,
                maxIdleTimeMS=int(self.idle_timeout * 1000)
            )
            self.client = client
            self.db = client[self.db_name]
        return self.db

    async def close(self):
        if self.client:
            self.client.close()
            self.client = None
            self.db = None

    def get_collection(self, collection_name):
        if not self.db:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self.db[collection_name]

    async def find_one(self, collection_name, query, *args, **kwargs):
        if not self.db:
            await self.connect()
        return await self.db[collection_name].find_one(query, *args, **kwargs)

    async def find_many(self, collection_name, query, *args, **kwargs):
        if not self.db:
            await self.connect()
        cursor = self.db[collection_name].find(query, *args, **kwargs)
        return await cursor.to_list(length=None)

    async def insert_one(self, collection_name, document):
        if not self.db:
            await self.connect()
        return await self.db[collection_name].insert_one(document)

    async def insert_many(self, collection_name, documents):
        if not self.db:
            await self.connect()
        return await self.db[collection_name].insert_many(documents)

    async def update_one(self, collection_name, filter, update, *args, **kwargs):
        if not self.db:
            await self.connect()
        return await self.db[collection_name].update_one(filter, update, *args, **kwargs)

    async def delete_one(self, collection_name, filter):
        if not self.db:
            await self.connect()
        return await self.db[collection_name].delete_one(filter)

    async def delete_many(self, collection_name, filter):
        if not self.db:
            await self.connect()
        return await self.db[collection_name].delete_many(filter)