from pathlib import Path
from uuid import uuid4
import shutil

from fastapi import UploadFile

from app.core.config import settings


class StorageService:
    """
    Handles storing uploaded files on the local filesystem.
    """

    def __init__(self) -> None:
        self.upload_dir = Path(settings.UPLOAD_DIR)

    def save_file(self, file: UploadFile) -> dict:
        """
        Save an uploaded file with a unique filename.

        Returns:
            Dictionary containing storage metadata.
        """

        extension = Path(file.filename).suffix

        stored_filename = f"{uuid4()}{extension}"

        destination = self.upload_dir / stored_filename

        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "original_filename": file.filename,
            "stored_filename": stored_filename,
            "file_path": str(destination),
            "content_type": file.content_type,
            "file_size": destination.stat().st_size,
        }