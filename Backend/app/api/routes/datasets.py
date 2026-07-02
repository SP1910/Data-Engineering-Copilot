from fastapi import APIRouter, File, UploadFile, status

from app.schemas.dataset import DatasetUploadResponse
from app.services.dataset_service import DatasetService

router = APIRouter(prefix="/datasets", tags=["Datasets"])

dataset_service = DatasetService()


@router.post(
    "/upload",
    response_model=DatasetUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_dataset(
    file: UploadFile = File(...),
) -> DatasetUploadResponse:
    """
    Upload a dataset.
    """

    return dataset_service.upload_dataset(file)