"""Load, validate, and split raw loan-application data."""

from pathlib import Path
import sys

import pandas as pd
from pandas.api.types import is_object_dtype, is_string_dtype
from sklearn.model_selection import train_test_split

from src.entity.config_entity import DataIngestionArtifact, DataIngestionConfig
from src.exception.exception import CreditRiskException
from src.logger.logger import logger
from src.utils.common import create_directories, save_json


class DataIngestion:
    """Create reproducible train and test datasets from the raw CSV file."""

    def __init__(self, config: DataIngestionConfig, schema: dict):
        self.config = config
        self.schema = schema

    def _validate_data(self, dataframe: pd.DataFrame) -> dict:
        """Validate essential fields and configured schema columns before splitting."""
        target = self.config.target_column
        required_columns = {target, "SK_ID_CURR"}
        missing_required = sorted(required_columns - set(dataframe.columns))
        if missing_required:
            raise ValueError(f"Raw data is missing required columns: {missing_required}")

        missing_schema_columns = sorted(set(self.schema) - set(dataframe.columns))
        if missing_schema_columns:
            raise ValueError(
                f"Raw data is missing columns declared in schema.yaml: {missing_schema_columns}"
            )

        invalid_dtypes = {}
        for column, definition in self.schema.items():
            expected_dtype = str(definition["type"])
            actual_dtype = str(dataframe[column].dtype)
            is_compatible_string = expected_dtype == "object" and (
                is_object_dtype(dataframe[column]) or is_string_dtype(dataframe[column])
            )
            if actual_dtype != expected_dtype and not is_compatible_string:
                invalid_dtypes[column] = {"expected": expected_dtype, "actual": actual_dtype}
        if invalid_dtypes:
            raise ValueError(f"Schema dtype mismatch: {invalid_dtypes}")

        target_values = set(dataframe[target].dropna().unique())
        if target_values - {0, 1}:
            raise ValueError(f"{target} must be binary (0/1); found {sorted(target_values)}")
        if len(target_values) < 2:
            raise ValueError(f"{target} must contain both default classes for a stratified split")
        if dataframe["SK_ID_CURR"].isna().any() or dataframe["SK_ID_CURR"].duplicated().any():
            raise ValueError("SK_ID_CURR must be present and unique in the raw dataset")

        return {
            "rows": int(len(dataframe)),
            "columns": int(dataframe.shape[1]),
            "duplicate_rows": int(dataframe.duplicated().sum()),
            "missing_values": int(dataframe.isna().sum().sum()),
            "target_distribution": {
                str(label): int(count)
                for label, count in dataframe[target].value_counts().sort_index().items()
            },
        }

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """Read raw data, validate it, stratify the split, and persist all outputs."""
        try:
            raw_path = Path(self.config.raw_data_path)
            if not raw_path.is_file():
                raise FileNotFoundError(f"Raw data file was not found: {raw_path}")
            if not 0 < self.config.test_size < 1:
                raise ValueError("test_size must be strictly between 0 and 1")

            logger.info("Reading raw training data from %s", raw_path)
            dataframe = pd.read_csv(raw_path)
            report = self._validate_data(dataframe)

            train_df, test_df = train_test_split(
                dataframe,
                test_size=self.config.test_size,
                random_state=self.config.random_state,
                stratify=dataframe[self.config.target_column],
            )
            create_directories([self.config.root_dir])
            train_df.to_csv(self.config.train_data_path, index=False)
            test_df.to_csv(self.config.test_data_path, index=False)

            report.update(
                {
                    "train_rows": int(len(train_df)),
                    "test_rows": int(len(test_df)),
                    "target_column": self.config.target_column,
                    "test_size": self.config.test_size,
                    "random_state": self.config.random_state,
                }
            )
            save_json(Path(self.config.validation_report_path), report)
            logger.info("Data ingestion completed: %s train rows, %s test rows", len(train_df), len(test_df))

            return DataIngestionArtifact(
                train_data_path=Path(self.config.train_data_path),
                test_data_path=Path(self.config.test_data_path),
                validation_report_path=Path(self.config.validation_report_path),
            )
        except Exception as error:
            raise CreditRiskException(error, sys) from error
