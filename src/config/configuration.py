"""Configuration factory for pipeline components."""

from src.constant import CONFIG_FILE_PATH, PARAMS_FILE_PATH, SCHEMA_FILE_PATH
from src.entity.config_entity import (
    DataIngestionConfig,
    DataTransformationConfig,
    DataValidationConfig,
    ModelTrainerConfig,
)
from src.exception.exception import CreditRiskException
from src.utils.common import create_directories, read_yaml

import sys


class ConfigurationManager:
    """Load project YAML files once and expose typed component settings."""

    def __init__(
        self,
        config_filepath=CONFIG_FILE_PATH,
        params_filepath=PARAMS_FILE_PATH,
        schema_filepath=SCHEMA_FILE_PATH,
    ):
        try:
            self.config = read_yaml(config_filepath)
            self.params = read_yaml(params_filepath)
            self.schema = read_yaml(schema_filepath)
            create_directories([self.config.artifacts_root])
        except Exception as error:
            raise CreditRiskException(error, sys) from error

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        """Create the configuration required to load and split training data."""
        try:
            ingestion = self.config.data_ingestion
            root_dir = ingestion.root_dir
            create_directories([root_dir])

            return DataIngestionConfig(
                root_dir=root_dir,
                raw_data_path=ingestion.raw_data_path,
                train_data_path=ingestion.train_data_path,
                test_data_path=ingestion.test_data_path,
                validation_report_path=f"{root_dir}/validation_report.json",
                target_column="TARGET",
                test_size=float(self.params.test_size),
                random_state=int(self.params.random_state),
            )
        except Exception as error:
            raise CreditRiskException(error, sys) from error

    def get_data_validation_config(self) -> DataValidationConfig:
        validation = self.config.data_validation
        create_directories([validation.root_dir])
        return DataValidationConfig(
            root_dir=validation.root_dir,
            validation_report_path=validation.validation_report_path,
            target_column="TARGET",
        )

    def get_data_transformation_config(self) -> DataTransformationConfig:
        transformation = self.config.data_transformation
        create_directories([transformation.root_dir])
        return DataTransformationConfig(
            root_dir=transformation.root_dir,
            preprocessor_path=transformation.preprocessor_path,
            train_data_path=transformation.train_data_path,
            test_data_path=transformation.test_data_path,
            target_column="TARGET",
            identifier_column="SK_ID_CURR",
        )

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        trainer = self.config.model_trainer
        parameters = self.params.model.logistic_regression
        create_directories([trainer.root_dir])
        return ModelTrainerConfig(
            root_dir=trainer.root_dir,
            model_path=trainer.model_path,
            metrics_path=trainer.metrics_path,
            random_state=int(self.params.random_state),
            C=float(parameters.C),
            max_iter=int(parameters.max_iter),
            class_weight=str(parameters.class_weight),
        )
