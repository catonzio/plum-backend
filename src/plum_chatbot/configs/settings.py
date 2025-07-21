import os
from threading import Lock


class Settings:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(Settings, cls).__new__(cls)
                    cls._instance._init_env()
        return cls._instance

    def _init_env(self):
        self.RUN_MODE: str = os.getenv("RUN_MODE", "dev")

        # --- QDRANT --- #
        self.QDRANT_READ_ONLY_API_KEY = os.getenv(
            "QDRANT__SERVICE__READ_ONLY_API_KEY", ""
        )
        self.QDRANT_API_KEY: str = os.getenv("QDRANT__SERVICE__API_KEY", "")
        self.QDRANT_HOST: str = "plum_database"  # os.getenv("QDRANT__SERVICE__HOST")
        self.QDRANT_HTTP_PORT: str = os.getenv("QDRANT__SERVICE__HTTP_PORT", "")
        self.QDRANT_COLLECTION_NAME: str = os.getenv(
            "QDRANT__SERVICE__COLLECTION_NAME", ""
        )
        self.QDRANT_URL: str = f"http://{self.QDRANT_HOST}:{self.QDRANT_HTTP_PORT}"

        # --- POSTGRES --- #
        self.POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
        self.POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")
        self.POSTGRES_DB: str = os.getenv("POSTGRES_DB", "database")
        self.POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "server")
        self.POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
        self.POSTGRES_URL: str = f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

        # --- LANGSMITH --- #
        self.LANGSMITH_API_KEY: str = os.getenv("LANGSMITH_API_KEY", "")

        self.DEFAULT_AGENT: str = os.getenv("DEFAULT_AGENT", "rag")

    def reload(self):
        """Reload environment variables (if they have changed)."""
        self._init_env()


# Usage:
if __name__ == "__main__":
    settings = Settings()
    print(settings.QDRANT_API_KEY)
