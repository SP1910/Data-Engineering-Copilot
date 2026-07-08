from pandas import DataFrame

from app.schemas.profile import (
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

        return DatasetQualityProfile(
            duplicate_rows=duplicate_rows,
            duplicate_percentage=duplicate_percentage,
            duplicate_columns=duplicate_columns,
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