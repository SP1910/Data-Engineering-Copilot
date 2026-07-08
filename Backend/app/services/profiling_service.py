from pathlib import Path

import pandas as pd
from fastapi import HTTPException, status
from pandas.errors import EmptyDataError, ParserError
from sqlalchemy.orm import Session

from app.analyzers.column_analyzer import ColumnAnalyzer
from app.repositories.dataset_repository import DatasetRepository
from app.schemas.profile import BasicDatasetProfile


class ProfilingService:
    """
    Service responsible for loading datasets and generating
    basic profiling information.
    """

    def __init__(self, db: Session):
        self.repository = DatasetRepository(db)
        self.column_analyzer = ColumnAnalyzer()

    def profile_dataset(self, dataset_id: int) -> BasicDatasetProfile:
        """
        Generate a basic profile for a dataset.
        """

        dataset = self.repository.get_by_id(dataset_id)

        if dataset is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dataset not found.",
            )

        csv_path = Path(dataset.file_path)

        if not csv_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dataset file not found on disk.",
            )

        try:
            dataframe = pd.read_csv(csv_path)

        except EmptyDataError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded CSV is empty.",
            )

        except ParserError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid CSV format.",
            )

        rows, columns = dataframe.shape

        memory_usage = int(
            dataframe.memory_usage(deep=True).sum()
        )

        column_profiles = [
            self.column_analyzer.analyze(dataframe[column])
            for column in dataframe.columns
        ]

        return BasicDatasetProfile(
            dataset_name=dataset.original_filename,
            rows=rows,
            columns=columns,
            memory_usage_bytes=memory_usage,
            column_profiles=column_profiles,
        )