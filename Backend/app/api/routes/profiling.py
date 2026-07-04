from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.profile import BasicDatasetProfile
from app.services.profiling_service import ProfilingService

router = APIRouter(
    prefix="/datasets",
    tags=["Dataset Profiling"],
)


@router.get(
    "/{dataset_id}/profile",
    response_model=BasicDatasetProfile,
    summary="Generate basic dataset profile",
)
def get_dataset_profile(
    dataset_id: int,
    db: Session = Depends(get_db),
) -> BasicDatasetProfile:
    """
    Generate a basic profile for an uploaded dataset.
    """

    profiling_service = ProfilingService(db)

    return profiling_service.profile_dataset(dataset_id)