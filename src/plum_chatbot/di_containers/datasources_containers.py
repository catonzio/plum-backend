from dependency_injector import containers, providers

from plum_chatbot.configs.settings import Settings
from plum_chatbot.datasources.parameters import PostgresParameters, QdrantParameters
from plum_chatbot.datasources.postgres_datasource import PostgresDatasource
from plum_chatbot.datasources.qdrant_datasource import QdrantDatasource


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    settings = Settings()

    qdrant = providers.Singleton(
        QdrantDatasource,
        config=QdrantParameters(
            model_name="llama3.2",
            model_url="host.docker.internal",
            qdrant_url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
            collection_name=settings.QDRANT_COLLECTION_NAME,
        ),
    )

    postgres = providers.Singleton(
        PostgresDatasource,
        config=PostgresParameters(postgres_url=settings.POSTGRES_URL),
    )

    # repository = providers.Singleton(Repository, datasource=datasource)
    # agent = providers.Singleton(Agent, repository=repository)


container = Container()


# Wrapper functions to avoid FastAPI's automatic parameter detection
def get_qdrant_datasource() -> QdrantDatasource:
    """Get QdrantDatasource instance from container."""
    return container.qdrant()


def get_postgres_datasource() -> PostgresDatasource:
    """Get PostgresDatasource instance from container."""
    return container.postgres()
