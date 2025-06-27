import logging
from asyncio import gather
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
        await setup(app)  # Perform any asynchronous startup tasks
        logger.info("Starting up the webserver...")
        yield
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise
    finally:
        await shutdown(app)
        logger.info("Shutting down the webserver...")


async def setup(app: FastAPI):
    """
    Placeholder for any asynchronous startup tasks.
    This can be used to initialize resources or perform checks.
    """
    logger.info("Initializing dependencies...")
    try:
        container.init_resources()
        providers = [
            provider.setup()  # type: ignore
            for provider in Container.providers.values()
            if isinstance(provider(), BaseDatasource)
        ]
        await gather(*providers)
    except Exception as e:
        logger.error(f"Error during startup: {e}", exc_info=True)
        raise
    logger.info("All dependencies initialized successfully.")


async def shutdown(app: FastAPI):
    """
    Placeholder for any asynchronous shutdown tasks.
    This can be used to clean up resources or perform final checks.
    """
    logger.info("Cleaning up dependencies...")
    try:
        providers = [
            provider.shutdown()  # type: ignore
            for provider in Container.providers.values()
            if isinstance(provider(), BaseDatasource)
        ]
        await gather(*providers)
        container.shutdown_resources()
    except Exception as e:
        logger.error(f"Error during shutdown: {e}", exc_info=True)
        raise
    logger.info("All dependencies cleaned up successfully.")
