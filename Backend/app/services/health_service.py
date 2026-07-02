from app.core.config import settings
from app.schemas.health import HealthResponse


class HealthService:
    """
    Service responsible for health-related operations.
    """

    @staticmethod
    def get_health_status() -> HealthResponse:
        """
        Return the application's health information.
        """

        return HealthResponse(
            status="healthy",
            application=settings.app_name,
            version=settings.app_version,
            environment=settings.environment,
        )