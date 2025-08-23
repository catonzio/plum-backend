import logging

# from langchain_ollama import OllamaEmbeddings
# from langchain_qdrant import QdrantVectorStore
import numpy as np
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from plum_chatbot.datasources.base_datasource import BaseDatasource
from plum_chatbot.datasources.models.qdrant_models import QdrantDocument
from plum_chatbot.datasources.parameters import QdrantParameters


class QdrantDatasource(BaseDatasource):
    """
    Datasource for Qdrant vector database.
    """

    embeddings_model: SentenceTransformer
    client: QdrantClient
    # vector_store: QdrantVectorStore
    embedding_model_name: str
    model_url: str
    qdrant_url: str
    api_key: str
    collection_name: str
    logger: logging.Logger

    def __init__(self, config: QdrantParameters):
        super().__init__(name="QdrantDatasource")
        self.embedding_model_name = config.embedding_model_name
        self.model_url = config.model_url
        self.qdrant_url = config.qdrant_url
        self.api_key = config.api_key
        self.collection_name = config.collection_name
        self.logger = logging.getLogger(__name__)

    async def setup(self):
        """
        Initialize the Qdrant client and ensure the collection exists.
        """
        # self.embeddings = OllamaEmbeddings(
        #     model=self.embedding_model_name, base_url=self.model_url
        # )
        self.embeddings_model = SentenceTransformer(self.embedding_model_name)

        self.client = QdrantClient(
            url=self.qdrant_url, api_key=self.api_key, https=True
        )

        # self.vector_store = QdrantVectorStore(
        #     client=self.client,
        #     collection_name=self.collection_name,
        #     embedding=self.embeddings,
        # )
        self.logger.info("Qdrant client initialized successfully.")

    async def shutdown(self):
        """
        Clean up the Qdrant client.
        """
        # self.vector_store._client.close()
        self.client.close()
        self.logger.info("Qdrant client shut down successfully.")

    # async def aquery(self, query: str, limit: int = 10, **kwargs):
    #     results = await self.vector_store.asimilarity_search(
    #         query=query,
    #         limit=limit,
    #     )
    #     return results

    def query(self, query: str, limit: int = 2, **kwargs) -> list[QdrantDocument]:
        # results = self.vector_store.similarity_search(
        #     query=query,
        #     limit=limit,
        # )
        embeddings: np.ndarray = np.array(
            self.embeddings_model.encode_query(query, show_progress_bar=False)
        )
        qresults = self.client.query_points(
            self.collection_name, query=embeddings, limit=limit
        )
        results = [
            QdrantDocument.model_validate(qr.payload) for qr in qresults.points or []
        ]
        return results
