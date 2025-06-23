import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from plum_chatbot.datasources.base_datasource import BaseDatasource
from plum_chatbot.di_containers.datasources_containers import Container, container

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Lifespan context manager for FastAPI app.
    Initializes or resets the vars dictionary and logs startup/shutdown events.
    """
    try:
        await up(app)  # Perform any asynchronous startup tasks
        logger.info("Starting up the webserver...")
        yield
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise
    finally:
        await down(app)
        logger.info("Shutting down the webserver...")


async def up(app: FastAPI):
    """
    Placeholder for any asynchronous startup tasks.
    This can be used to initialize resources or perform checks.
    """
    logger.info("Initializing dependencies...")
    container.init_resources()
    for k, v in Container.providers.items():
        provider = v()
        if isinstance(provider, BaseDatasource):
            provider.setup()
        logger.info(f"Dependency {k} initialized with {v}")
    # mount_gradio(app)


async def down(app: FastAPI):
    """
    Placeholder for any asynchronous shutdown tasks.
    This can be used to clean up resources or perform final checks.
    """
    for k, v in Container.providers.items():
        provider = v()
        if isinstance(provider, BaseDatasource):
            provider.shutdown()
