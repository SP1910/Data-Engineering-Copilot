from pydantic import BaseModel


class ColumnProfile(BaseModel):
    """
    Basic information about a single dataset column.
    """

    name: str
    pandas_dtype: str
    semantic_type: str


class BasicDatasetProfile(BaseModel):
    """
    Basic profile information for an uploaded dataset.
    """

    dataset_name: str
    rows: int
    columns: int
    memory_usage_bytes: int
    column_profiles: list[ColumnProfile]