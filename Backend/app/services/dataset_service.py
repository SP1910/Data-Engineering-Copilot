from fastapi import UploadFile

from app.schemas.dataset import DatasetUploadResponse
from app.services.storage_service import StorageService


class DatasetService:
    """
    Handles dataset-related business logic.
    """

    ALLOWED_EXTENSIONS = {".csv"}

    def __init__(self) -> None:
        self.storage_service = StorageService()

    def upload_dataset(
        self,
        file: UploadFile,
    ) -> DatasetUploadResponse:
        """
        Validate and store a dataset.
        """

        self._validate_extension(file)

        metadata = self.storage_service.save_file(file)

        return DatasetUploadResponse(**metadata)

    def _validate_extension(
        self,
        file: UploadFile,
    ) -> None:
        """
        Ensure only supported dataset formats are uploaded.
        """

        if file.filename is None:
            raise ValueError("Filename is missing.")

        extension = file.filename.lower().split(".")[-1]

        extension = f".{extension}"

        if extension not in self.ALLOWED_EXTENSIONS:
            raise ValueError(
                "Only CSV files are supported."
            )