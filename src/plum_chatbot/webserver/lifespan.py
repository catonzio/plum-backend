import logging
from asyncio import gather
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from plum_chatbot.configs.logger import setup_global_logging
from plum_chatbot.di_containers.datasources_containers import container

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
    # Setup global logging configuration first
    setup_global_logging()
    logger.info("Initializing dependencies...")
    try:
        container.init_resources()

        # Initialize datasources by calling setup on the singleton instances
        qdrant_datasource = container.qdrant()
        postgres_datasource = container.postgres()

        await gather(qdrant_datasource.setup(), postgres_datasource.setup())
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
        # Shutdown datasources by calling shutdown on the singleton instances
        qdrant_datasource = container.qdrant()
        postgres_datasource = container.postgres()

        await gather(qdrant_datasource.shutdown(), postgres_datasource.shutdown())
        container.shutdown_resources()
    except Exception as e:
        logger.error(f"Error during shutdown: {e}", exc_info=True)
        raise
    logger.info("All dependencies cleaned up successfully.")
