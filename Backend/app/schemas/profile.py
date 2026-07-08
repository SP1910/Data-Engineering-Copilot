from enum import Enum

from pydantic import BaseModel


class SemanticType(str, Enum):
    NUMERICAL = "numerical"
    CATEGORICAL = "categorical"
    BOOLEAN = "boolean"
    DATETIME = "datetime"
    TEXT = "text"


class DataQualityProfile(BaseModel):
    """
    Data quality metrics for a column.
    """

    missing_count: int
    missing_percentage: float
    unique_values: int
    is_constant: bool
    is_identifier: bool


class NumericStatistics(BaseModel):
    count: int
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
    semantic_type: SemanticType

    data_quality: DataQualityProfile

    statistics: NumericStatistics | None


class BasicDatasetProfile(BaseModel):
    dataset_name: str
    rows: int
    columns: int
    memory_usage_bytes: int

    column_profiles: list[ColumnProfile]