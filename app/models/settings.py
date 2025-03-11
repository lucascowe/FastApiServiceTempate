import os
import logging

from pydantic import model_validator, Field
from pydantic_settings import BaseSettings
from typing import Optional, Dict


logger = logging.getLogger(__name__)


class DatabaseSettings(BaseSettings):
    name: str
    port: int
    user: Optional[str] = None
    password: Optional[str] = None
    db_name: Optional[str] = None


class Settings(BaseSettings):
    server_name: str
    version: str
    api_version: str
    internal_port: int
    external_port: int

    # Database settings
    databases: Optional[Dict[str, DatabaseSettings]] = Field(default_factory=dict)

    class Config:
        env_file = ".env" if os.path.isfile(".env") else None
        env_file_encoding = "utf-8"
        extra = "allow"
        env_nested_delimiter = "__"

    @model_validator(mode='before')
    def load_databases(cls, values):
        # Initialize databases if not present
        db_list = ['postgres', 'mongo', 'redis']
        logger.info(f"values are: {values}")
        logger.info(f"env file is {os.path.isfile('.env')}")
        if os.path.isfile(".env") is False:
            db_envs = {
                k.lower(): v for k, v in os.environ.items() if any(db in k.lower() for db in db_list)
            }
        else:
            db_envs = values
        if 'databases' not in values:
            values['databases'] = {}

        # Find all potential database prefixes from values
        db_prefixes = set()

        for key in db_envs:
            if '_port' in key.lower():
                prefix = key.split('_')[0].lower()
                if prefix in db_list:
                    db_prefixes.add(prefix)

        logger.info(f"Processing databases: {db_prefixes} from {db_envs}")
        # Build database settings for each identified database
        for prefix in db_prefixes:
            port_key = f"{prefix}_port"
            user_key = f"{prefix}_user"
            password_key = f"{prefix}_password"
            name_key = f"{prefix}_db"

            if port_key in db_envs:
                db_settings = DatabaseSettings(
                    name=prefix,
                    port=int(db_envs[port_key]),
                    user=db_envs.get(user_key),
                    password=db_envs.get(password_key),
                    db_name=db_envs.get(name_key, prefix),
                )
                values['databases'][prefix] = db_settings
        logger.info(f"DBS: {values['databases'].keys()}")
        return values


settings = Settings()