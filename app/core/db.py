import logging

from fastapi import FastAPI
from app.core.config import settings
from app.core.databases.mongo_connection_manager import MongoConnectionManager
from app.core.databases.postgres_connection_manager import PostgresConnectionManager
from app.core.databases.redis_connection_manager import RedisConnectionManager

logger = logging.getLogger(__name__)


async def connect_db(app: FastAPI):
    db_connections = {
        'redis': RedisConnectionManager,
        'mongo': MongoConnectionManager,
        'postgres': PostgresConnectionManager
    }
    for db, db_settings in settings.databases.items():
        if db not in db_connections:
            raise ConnectionError(f"Connection to {db} not configure")
        setattr(
            app.state,
            db,
            db_connections[db](db_settings.user, db_settings.password, db_settings.port, db_settings.db_name)
        )
        logger.info(f"Set {db} connection")


async def close_db(app: FastAPI):
    db_close_map = {
        "mongo": lambda client: client.close(),  # Not async
        "redis": lambda client: client.close(),  # Async
        "pg_pool": lambda client: client.close()  # Async
    }

    # Handle all database connections
    for db_name, close_func in db_close_map.items():
        if hasattr(app.state, db_name):
            db_client = getattr(app.state, db_name)
            if db_client:
                close_result = close_func(db_client)
                # If it's an awaitable, await it
                if hasattr(close_result, "__await__"):
                    await close_result
