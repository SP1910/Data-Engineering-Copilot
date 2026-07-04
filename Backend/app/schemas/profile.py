from pydantic import BaseModel


class BasicDatasetProfile(BaseModel):
    dataset_name: str
    rows: int
    columns: int
    memory_usage_bytes: int
    column_names: list[str]