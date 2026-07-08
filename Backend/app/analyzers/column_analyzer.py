from pandas.api.types import (
    is_bool_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
)

from pandas import Series

from app.schemas.profile import ColumnProfile


class ColumnAnalyzer:
    """
    Responsible for analyzing a single dataframe column.
    """

    def analyze(self, column: Series) -> ColumnProfile:
        """
        Analyze a dataframe column and return its profile.
        """

        return ColumnProfile(
            name=column.name,
            pandas_dtype=str(column.dtype),
            semantic_type=self._infer_semantic_type(column),
        )

    def _infer_semantic_type(self, column: Series) -> str:
        """
        Infer the semantic type of a dataframe column.
        """

        # Boolean columns
        if is_bool_dtype(column):
            return "boolean"

        # Numeric columns
        if is_numeric_dtype(column):
            return "numerical"

        # Datetime columns
        if is_datetime64_any_dtype(column):
            return "datetime"

        # Object columns
        return self._analyze_object_column(column)

    def _analyze_object_column(self, column: Series) -> str:
        """
        Analyze object/string columns.
        """

        non_null = column.dropna()

        # Empty column
        if non_null.empty:
            return "categorical"

        # Try datetime conversion
        try:
            converted = pd.to_datetime(
                non_null,
                errors="coerce",
            )

            if converted.notna().all():
                return "datetime"

        except Exception:
            pass

        average_length = non_null.astype(str).str.len().mean()

        if average_length > 50:
            return "text"

        return "categorical"