from pydantic import BaseModel


class NumericStatistics(BaseModel):
    count: int
    unique_values: int
    mean: float
    median: float
    std: float
    minimum: float
    maximum: float
    q1: float
    q3: float


class ColumnProfile(BaseModel):
    name: str
    pandas_dtype: str
    semantic_type: str

    missing_count: int
    missing_percentage: float

    statistics: NumericStatistics | None


class BasicDatasetProfile(BaseModel):
    dataset_name: str
    rows: int
    columns: int
    memory_usage_bytes: int

    column_profiles: list[ColumnProfile]