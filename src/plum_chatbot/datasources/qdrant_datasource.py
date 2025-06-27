from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

from plum_chatbot.datasources.base_datasource import BaseDatasource
from plum_chatbot.datasources.parameters import QdrantParameters


class QdrantDatasource(BaseDatasource):
    """
    Datasource for Qdrant vector database.
    """

    embeddings: OllamaEmbeddings
    client: QdrantClient
    vector_store: QdrantVectorStore
    model_name: str
    model_url: str
    qdrant_url: str
    api_key: str
    collection_name: str

    def __init__(self, config: QdrantParameters):
        super().__init__(name="QdrantDatasource")
        self.model_name = config.model_name
        self.model_url = config.model_url
        self.qdrant_url = config.qdrant_url
        self.api_key = config.api_key
        self.collection_name = config.collection_name

    async def setup(self):
        """
        Initialize the Qdrant client and ensure the collection exists.
        """
        self.embeddings = OllamaEmbeddings(
            model=self.model_name, base_url=self.model_url
        )

        self.client = QdrantClient(
            url=self.qdrant_url, api_key=self.api_key, https=True
        )

        self.vector_store = QdrantVectorStore(
            client=self.client,
            collection_name=self.collection_name,
            embedding=self.embeddings,
        )

    async def shutdown(self):
        """
        Clean up the Qdrant client.
        """
        self.vector_store._client.close()
        self.client.close()

    async def aquery(self, query: str, limit: int = 10, **kwargs):
        results = await self.vector_store.asimilarity_search(
            query=query,
            limit=limit,
        )
        return results

    def query(self, query: str, limit: int = 10, **kwargs):
        results = self.vector_store.similarity_search(
            query=query,
            limit=limit,
        )
        return results
