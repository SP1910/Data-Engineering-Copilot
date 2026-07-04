from sqlalchemy.orm import Session

from app.models.dataset import Dataset


class DatasetRepository:
    """
    Handles all database operations related to datasets.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, dataset: Dataset) -> Dataset:
        """
        Persist a dataset to the database.
        """

        self.db.add(dataset)
        self.db.commit()
        self.db.refresh(dataset)

        return dataset

    def get_by_id(self, dataset_id: int) -> Dataset | None:
        """
        Retrieve a dataset by its primary key.

        Returns:
            Dataset if found, otherwise None.
        """

        return (
            self.db.query(Dataset)
            .filter(Dataset.id == dataset_id)
            .first()
        )