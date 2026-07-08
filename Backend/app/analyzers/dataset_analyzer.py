from pandas import DataFrame

from app.schemas.profile import DatasetQualityProfile


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

        return DatasetQualityProfile(
            duplicate_rows=duplicate_rows,
            duplicate_percentage=duplicate_percentage,
        )

    def analyze_duplicate_rows(
        self,
        dataframe: DataFrame,
    ) -> int:
        """
        Count duplicate rows in the dataset.
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