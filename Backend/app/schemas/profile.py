from enum import Enum

from pydantic import BaseModel

class DuplicateColumnPair(BaseModel):
    """
    Represents a pair of duplicate columns.
    """

    original: str
    duplicate: str


class SemanticType(str, Enum):
    NUMERICAL = "numerical"
    CATEGORICAL = "categorical"
    BOOLEAN = "boolean"
    DATETIME = "datetime"
    TEXT = "text"


class DataQualityProfile(BaseModel):
    """
    Data quality metrics for a single column.
    """

    missing_count: int
    missing_percentage: float

    unique_values: int

    is_constant: bool
    is_identifier: bool
    is_high_cardinality: bool


class DatasetQualityProfile(BaseModel):
    """
    Dataset-level quality metrics.
    """

    duplicate_rows: int
    duplicate_percentage: float

    duplicate_columns: list[DuplicateColumnPair]


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

    dataset_quality: DatasetQualityProfile

    column_profiles: list[ColumnProfile]