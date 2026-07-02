from fastapi import FastAPI

from app.api.root import api_router
from app.core.config import settings
from app.core.lifespan import lifespan


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """

    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    application.include_router(api_router)

    return application


app = create_application()