from fastapi import APIRouter

from app.api.routes.datasets import router as datasets_router
from app.api.routes.profiling import router as profiling_router
from app.api.v1.endpoints.health import router as health_router

router = APIRouter()

# Health Endpoints
router.include_router(
    health_router,
    prefix="/health",
    tags=["Health"],
)

# Dataset Endpoints
router.include_router(
    datasets_router,
    tags=["Datasets"],
)

# Dataset Profiling Endpoints
router.include_router(
    profiling_router,
    tags=["Dataset Profiling"],
) 