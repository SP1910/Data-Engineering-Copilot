from fastapi import FastAPI

from app.api.router import api_router
from app.api.routes import datasets
from app.core.config import settings
from app.core.lifespan import lifespan
from app.core.storage import initialize_storage


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """
    initialize_storage()    #initailize storage before application starts accept requests

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
    # application.include_router(
    #     datasets.router,
    #     prefix=settings.API_V1_STR,
    # )

    return application


app = create_application()