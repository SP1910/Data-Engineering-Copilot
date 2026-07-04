from pathlib import Path

import pandas as pd
from fastapi import HTTPException, status
from pandas.errors import EmptyDataError, ParserError
from sqlalchemy.orm import Session

from app.repositories.dataset_repository import DatasetRepository
from app.schemas.profile import BasicDatasetProfile


class ProfilingService:
    """
    Service responsible for loading datasets and generating
    basic profiling information.
    """

    def __init__(self, db: Session):
        self.repository = DatasetRepository(db)

    def profile_dataset(self, dataset_id: int) -> BasicDatasetProfile:
        """
        Load a dataset and generate a basic profile.
        """

        # Step 1: Fetch dataset metadata
        dataset = self.repository.get_by_id(dataset_id)

        if dataset is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dataset not found.",
            )

        # Step 2: Verify the file exists
        csv_path = Path(dataset.file_path)

        if not csv_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dataset file not found on disk.",
            )

        # Step 3: Read the CSV
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

        # Step 4: Extract basic information
        rows, columns = dataframe.shape

        memory_usage = int(
            dataframe.memory_usage(deep=True).sum()
        )

        column_names = dataframe.columns.tolist()

        # Step 5: Return response schema
        return BasicDatasetProfile(
            dataset_name=dataset.original_filename,
            rows=rows,
            columns=columns,
            memory_usage_bytes=memory_usage,
            column_names=column_names,
        )