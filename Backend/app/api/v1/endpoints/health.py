from fastapi import APIRouter, Depends

from app.dependencies.services import get_health_service
from app.schemas.health import HealthResponse
from app.services.health_service import HealthService

router = APIRouter()


@router.get(
    "",
    response_model=HealthResponse,
    summary="Health Check",
)
async def health_check(
    service: HealthService = Depends(get_health_service),
) -> HealthResponse:
    """
    Returns the current health status.
    """

    return service.get_health_status()