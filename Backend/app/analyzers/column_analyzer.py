import pandas as pd
from pandas import Series
from pandas.api.types import (
    is_bool_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
)

from app.schemas.profile import (
    ColumnProfile,
    DataQualityProfile,
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

        if cleaned_column.empty:
            return NumericStatistics(
                count=0,
                mean=0.0,
                median=0.0,
                std=0.0,
                minimum=0.0,
                maximum=0.0,
                q1=0.0,
                q3=0.0,
            )

        return NumericStatistics(
            count=int(cleaned_column.count()),
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

        unique_values = self._calculate_unique_values(column)

        data_quality = DataQualityProfile(
            missing_count=missing_count,
            missing_percentage=missing_percentage,
            unique_values=unique_values,
            is_constant=self._is_constant_column(column),
            is_identifier=self._is_identifier(column, unique_values),
        )

        statistics = None

        if semantic_type == SemanticType.NUMERICAL:
            statistics = self.statistics_analyzer.analyze(column)

        return ColumnProfile(
            name=column.name,
            pandas_dtype=str(column.dtype),
            semantic_type=semantic_type,
            data_quality=data_quality,
            statistics=statistics,
        )

    def _infer_semantic_type(self, column: Series) -> SemanticType:
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

    def _analyze_object_column(self, column: Series) -> SemanticType:
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

    def _calculate_unique_values(self, column: Series) -> int:
        """
        Calculate the number of unique non-null values.
        """

        return int(column.nunique(dropna=True))
    
    def _is_constant_column(self, column: Series) -> bool:
        """
        Determine whether a column contains only one unique
        non-null value.
        """

        return column.nunique(dropna=True) <= 1
    
    def _is_identifier(self, column:Series, unique_values:int) -> bool:

        non_null_count = int(column.count())

        if(non_null_count<10):
            return False
        
        return unique_values == non_null_count