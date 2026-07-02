from fastapi import APIRouter

from app.schemas.health import HealthResponse
from app.services.health_service import HealthService

router = APIRouter()


@router.get(
    "",
    response_model=HealthResponse,
    summary="Health Check",
)
async def health_check() -> HealthResponse:
    """
    Returns the current health status.
    """

    return HealthService.get_health_status()