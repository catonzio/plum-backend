class QdrantParameters:
    def __init__(
        self,
        model_name: str = "llama3.2",
        model_url: str = "host.docker.internal",
        qdrant_url: str = "http://localhost:6333",
        api_key: str = "",
        collection_name: str = "FAQ",
    ):
        self.model_name = model_name
        self.model_url = model_url
        self.qdrant_url = qdrant_url
        self.api_key = api_key
        self.collection_name = collection_name


class PostgresParameters:
    def __init__(
        self, postgres_url: str = "postgresql://user:password@localhost/dbname"
    ):
        self.postgres_url = postgres_url
