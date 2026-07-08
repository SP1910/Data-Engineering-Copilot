import pandas as pd
from pandas import Series
from pandas.api.types import (
    is_bool_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
)

from app.schemas.profile import (
    ColumnProfile,
    NumericStatistics,
    SemanticType,
)


class StatisticsAnalyzer:
    """
    Responsible for generating descriptive statistics
    for numerical columns.
    """

    def analyze(self, column: Series) -> NumericStatistics:
        """
        Generate descriptive statistics for a numerical column.
        """

        cleaned_column = column.dropna()

        return NumericStatistics(
            count=int(cleaned_column.count()),
            unique_values=int(cleaned_column.nunique()),
            mean=round(float(cleaned_column.mean()), 2),
            median=round(float(cleaned_column.median()), 2),
            std=round(float(cleaned_column.std()), 2),
            minimum=round(float(cleaned_column.min()), 2),
            maximum=round(float(cleaned_column.max()), 2),
            q1=round(float(cleaned_column.quantile(0.25)), 2),
            q3=round(float(cleaned_column.quantile(0.75)), 2),
        )


class ColumnAnalyzer:
    """
    Responsible for analyzing a single dataframe column.
    """

    def __init__(self):
        self.statistics_analyzer = StatisticsAnalyzer()

    def analyze(self, column: Series) -> ColumnProfile:
        """
        Analyze a dataframe column and return its profile.
        """

        semantic_type = self._infer_semantic_type(column)

        missing_count = self._calculate_missing_count(column)

        missing_percentage = self._calculate_missing_percentage(
            column,
            missing_count,
        )

        statistics = None

        if semantic_type == SemanticType.NUMERICAL:
            statistics = self.statistics_analyzer.analyze(column)

        return ColumnProfile(
            name=column.name,
            pandas_dtype=str(column.dtype),
            semantic_type=semantic_type,
            missing_count=missing_count,
            missing_percentage=missing_percentage,
            statistics=statistics,
        )

    def _infer_semantic_type(self, column: Series) -> str:
        """
        Infer the semantic type of a dataframe column.
        """

        if is_bool_dtype(column):
            return SemanticType.BOOLEAN

        if is_numeric_dtype(column):
            return SemanticType.NUMERICAL

        if is_datetime64_any_dtype(column):
            return SemanticType.DATETIME

        return self._analyze_object_column(column)

    def _analyze_object_column(self, column: Series) -> str:
        """
        Analyze object/string columns.
        """

        non_null = column.dropna()

        if non_null.empty:
            return SemanticType.CATEGORICAL

        converted = pd.to_datetime(
            non_null,
            errors="coerce",
        )

        if converted.notna().all():
            return SemanticType.DATETIME

        average_length = non_null.astype(str).str.len().mean()

        if average_length > 50:
            return SemanticType.TEXT

        return SemanticType.CATEGORICAL

    def _calculate_missing_count(self, column: Series) -> int:
        """
        Calculate the number of missing values.
        """

        return int(column.isna().sum())

    def _calculate_missing_percentage(
        self,
        column: Series,
        missing_count: int,
    ) -> float:
        """
        Calculate the percentage of missing values.
        """

        total_rows = len(column)

        if total_rows == 0:
            return 0.0

        return round((missing_count / total_rows) * 100, 2)