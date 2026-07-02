from pydantic import BaseModel


class DatasetUploadResponse(BaseModel):
    """
    Response returned after a dataset is successfully uploaded.
    """

    original_filename: str
    stored_filename: str
    file_path: str
    content_type: str | None
    file_size: int