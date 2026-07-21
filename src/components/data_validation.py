"""Data-quality checks performed after the train/test split."""

from pathlib import Path
import sys

import pandas as pd

from src.entity.config_entity import DataValidationConfig
from src.exception.exception import CreditRiskException
from src.utils.common import save_json


class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate(self, train_path: Path, test_path: Path) -> Path:
        try:
            train_df, test_df = pd.read_csv(train_path), pd.read_csv(test_path)
            checks = {}
            for name, dataframe in {"train": train_df, "test": test_df}.items():
                if self.config.target_column not in dataframe:
                    raise ValueError(f"{name} data is missing {self.config.target_column}")
                if dataframe[self.config.target_column].isna().any():
                    raise ValueError(f"{name} data has missing target values")
                if dataframe["SK_ID_CURR"].duplicated().any():
                    raise ValueError(f"{name} data has duplicate SK_ID_CURR values")
                for numeric_column in ("AMT_INCOME_TOTAL", "AMT_CREDIT"):
                    if numeric_column in dataframe and (dataframe[numeric_column] < 0).any():
                        raise ValueError(f"{name} data has negative values in {numeric_column}")
                checks[name] = {
                    "rows": int(len(dataframe)),
                    "duplicate_rows": int(dataframe.duplicated().sum()),
                    "missing_values": int(dataframe.isna().sum().sum()),
                    "default_rate": float(dataframe[self.config.target_column].mean()),
                }
            checks["status"] = "passed"
            report_path = Path(self.config.validation_report_path)
            save_json(report_path, checks)
            return report_path
        except Exception as error:
            raise CreditRiskException(error, sys) from error
