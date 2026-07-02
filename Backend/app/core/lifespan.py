from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage the application's startup and shutdown lifecycle.
    """

    logger.info("Starting Data Engineering Copilot backend...")

    # Future startup tasks:
    # - Connect to PostgreSQL
    # - Initialize Redis
    # - Load AI models
    # - Verify storage directories
    # - Initialize metrics

    logger.info("Application startup completed.")

    yield

    logger.info("Shutting down Data Engineering Copilot backend...")

    # Future shutdown tasks:
    # - Close database connections
    # - Close Redis
    # - Release resources

    logger.info("Application shutdown completed.")