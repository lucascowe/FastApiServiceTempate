from abc import ABC, abstractmethod


class BaseConnectionManager(ABC):
    def __init__(self, user, password, port, db_name, host=None, min_pool_size=5, max_pool_size=10, idle_timeout=300.0):
        self.name = self._get_name()
        self.host = host if host else self.name
        self.port = port
        self.db_name = db_name
        self.min_pool_size = min_pool_size
        self.max_pool_size = max_pool_size
        self.idle_timeout = idle_timeout
        self.pool = None
        self._user = user
        self._password = password
        self.uri = self._build_uri()

    @abstractmethod
    def _get_name(self):
        """Return the name of the database system"""
        pass

    def _build_uri(self):
        return f"{self.name}://{self._user}:{self._password}@{self.host}:{self.port}/{self.db_name}"

    @abstractmethod
    async def connect(self):
        """Connect to the database"""
        pass

    @abstractmethod
    async def close(self):
        """Close the database connection"""
        pass