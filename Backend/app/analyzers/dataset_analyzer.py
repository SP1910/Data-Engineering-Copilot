from pandas import DataFrame
from app.core.config import settings

from app.schemas.profile import (
    CorrelatedFeaturePair,
    DatasetQualityProfile,
    DuplicateColumnPair,
)


class DatasetAnalyzer:
    """
    Responsible for analyzing dataset-level quality metrics.
    """

    def analyze(self, dataframe: DataFrame) -> DatasetQualityProfile:
        """
        Analyze the dataset and return dataset-level quality metrics.
        """

        duplicate_rows = self.analyze_duplicate_rows(dataframe)

        duplicate_percentage = self.calculate_duplicate_percentage(
            dataframe,
            duplicate_rows,
        )

        duplicate_columns = self.analyze_duplicate_columns(
            dataframe,
        )

        highly_correlated_features = self.analyze_correlations(
            dataframe,
        )

        return DatasetQualityProfile(
            duplicate_rows=duplicate_rows,
            duplicate_percentage=duplicate_percentage,
            duplicate_columns=duplicate_columns,
            highly_correlated_features=highly_correlated_features,
        )

    def analyze_duplicate_rows(
        self,
        dataframe: DataFrame,
    ) -> int:
        """
        Count duplicate rows.
        """

        return int(dataframe.duplicated().sum())

    def calculate_duplicate_percentage(
        self,
        dataframe: DataFrame,
        duplicate_rows: int,
    ) -> float:
        """
        Calculate duplicate row percentage.
        """

        total_rows = len(dataframe)

        if total_rows == 0:
            return 0.0

        return round(
            (duplicate_rows / total_rows) * 100,
            2,
        )

    def analyze_duplicate_columns(
        self,
        dataframe: DataFrame,
    ) -> list[DuplicateColumnPair]:
        """
        Find duplicate columns in the dataset.
        """

        duplicate_columns = []

        columns = dataframe.columns

        for i in range(len(columns)):
            for j in range(i + 1, len(columns)):

                first_column = columns[i]
                second_column = columns[j]

                if dataframe[first_column].equals(
                    dataframe[second_column]
                ):
                    duplicate_columns.append(
                        DuplicateColumnPair(
                            original=first_column,
                            duplicate=second_column,
                        )
                    )

        return duplicate_columns
    
    def analyze_correlations(
        self,
        dataframe: DataFrame,
    ) -> list[CorrelatedFeaturePair]:
        """
        Detect highly correlated numerical feature pairs.
        """

        numeric_dataframe = dataframe.select_dtypes(include="number")

        if numeric_dataframe.shape[1] < 2:
            return []

        correlation_matrix = numeric_dataframe.corr()

        correlated_features = []

        columns = correlation_matrix.columns

        threshold = settings.CORRELATION_THRESHOLD

        for i in range(len(columns)):
            for j in range(i + 1, len(columns)):

                correlation = correlation_matrix.iloc[i, j]

                if abs(correlation) >= threshold:

                    correlated_features.append(
                        CorrelatedFeaturePair(
                            feature_1=columns[i],
                            feature_2=columns[j],
                            correlation=round(float(correlation), 2),
                        )
                    )

        return correlated_features