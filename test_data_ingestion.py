"""Unit tests for raw-data validation and stratified splitting."""

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import pandas as pd

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.data_validation import DataValidation
from src.components.model_trainer import ModelTrainer
from src.entity.config_entity import (
    DataIngestionConfig,
    DataTransformationConfig,
    DataValidationConfig,
    ModelTrainerConfig,
)


class TestDataIngestion(unittest.TestCase):
    def test_ingestion_splits_data_and_writes_report(self):
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "raw.csv"
            dataframe = pd.DataFrame(
                {
                    "TARGET": [0, 1] * 10,
                    "SK_ID_CURR": range(100000, 100020),
                    "AMT_INCOME_TOTAL": [100000.0] * 20,
                    "AMT_CREDIT": [200000.0] * 20,
                    "NAME_CONTRACT_TYPE": ["Cash loans"] * 20,
                }
            )
            dataframe.to_csv(source, index=False)
            config = DataIngestionConfig(
                root_dir=root / "artifacts",
                raw_data_path=source,
                train_data_path=root / "artifacts" / "train.csv",
                test_data_path=root / "artifacts" / "test.csv",
                validation_report_path=root / "artifacts" / "validation_report.json",
                target_column="TARGET",
                test_size=0.2,
                random_state=42,
            )
            schema = {
                "TARGET": {"type": "int64"},
                "SK_ID_CURR": {"type": "int64"},
                "AMT_INCOME_TOTAL": {"type": "float64"},
                "AMT_CREDIT": {"type": "float64"},
                "NAME_CONTRACT_TYPE": {"type": "object"},
            }

            artifact = DataIngestion(config, schema).initiate_data_ingestion()

            self.assertEqual(len(pd.read_csv(artifact.train_data_path)), 16)
            self.assertEqual(len(pd.read_csv(artifact.test_data_path)), 4)
            with artifact.validation_report_path.open() as file:
                self.assertEqual(json.load(file)["rows"], 20)

    def test_validation_transformation_and_baseline_model(self):
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "raw.csv"
            dataframe = pd.DataFrame({
                "TARGET": [0, 1] * 20,
                "SK_ID_CURR": range(40),
                "AMT_INCOME_TOTAL": [100000.0, 200000.0] * 20,
                "AMT_CREDIT": [50000.0, 250000.0] * 20,
                "NAME_CONTRACT_TYPE": ["Cash loans", "Revolving loans"] * 20,
            })
            dataframe.to_csv(source, index=False)
            ingestion_config = DataIngestionConfig(
                root / "ingestion", source, root / "ingestion" / "train.csv", root / "ingestion" / "test.csv",
                root / "ingestion" / "report.json", "TARGET", 0.25, 42,
            )
            schema = {column: {"type": dtype} for column, dtype in {
                "TARGET": "int64", "SK_ID_CURR": "int64", "AMT_INCOME_TOTAL": "float64",
                "AMT_CREDIT": "float64", "NAME_CONTRACT_TYPE": "object",
            }.items()}
            ingestion_artifact = DataIngestion(ingestion_config, schema).initiate_data_ingestion()
            report = DataValidation(DataValidationConfig(root / "validation", root / "validation" / "report.json", "TARGET")).validate(
                ingestion_artifact.train_data_path, ingestion_artifact.test_data_path
            )
            transformation_config = DataTransformationConfig(
                root / "transformation", root / "transformation" / "preprocessor.joblib",
                root / "transformation" / "train.joblib", root / "transformation" / "test.joblib", "TARGET", "SK_ID_CURR",
            )
            train_features, test_features = DataTransformation(transformation_config).initiate_data_transformation(
                ingestion_artifact.train_data_path, ingestion_artifact.test_data_path
            )
            model_path = ModelTrainer(ModelTrainerConfig(
                root / "models", root / "models" / "model.joblib", root / "models" / "metrics.json", 42, 1.0, 100, "balanced",
            )).initiate_model_trainer(train_features, test_features)
            self.assertTrue(report.is_file())
            self.assertTrue(model_path.is_file())


if __name__ == "__main__":
    unittest.main()
