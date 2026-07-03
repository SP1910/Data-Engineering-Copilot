from pathlib import Path

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.models.dataset import Dataset
from app.repositories.dataset_repository import DatasetRepository
from app.schemas.dataset import DatasetUploadResponse
from app.services.storage_service import StorageService


class DatasetService:

    ALLOWED_EXTENSIONS = {".csv"}

    def __init__(self, db: Session):
        self.storage_service = StorageService()
        self.repository = DatasetRepository(db)

    def upload_dataset(
        self,
        file: UploadFile,
    ) -> DatasetUploadResponse:

        self._validate_extension(file)

        metadata = self.storage_service.save_file(file)

        try:
            dataset = Dataset(**metadata)

            dataset = self.repository.create(dataset)

        except Exception:
            Path(metadata["file_path"]).unlink(missing_ok=True)
            raise

        return DatasetUploadResponse(
            original_filename=dataset.original_filename,
            stored_filename=dataset.stored_filename,
            file_path=dataset.file_path,
            content_type=dataset.content_type,
            file_size=dataset.file_size,
        )
    
    def _validate_extension(self, file: UploadFile) -> None:
        """
        Validate that the uploaded file has a supported extension.
        """

        extension = Path(file.filename).suffix.lower()

        if extension not in self.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Unsupported file type '{extension}'. "
                    f"Allowed types: {', '.join(self.ALLOWED_EXTENSIONS)}"
                ),
            )