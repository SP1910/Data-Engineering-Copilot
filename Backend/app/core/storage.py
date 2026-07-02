from pathlib import Path

from app.core.config import settings


def initialize_storage() -> None:
    """
    Create the upload directory if it doesn't already exist.
    """
    upload_path = Path(settings.UPLOAD_DIR)
    upload_path.mkdir(parents=True, exist_ok=True)