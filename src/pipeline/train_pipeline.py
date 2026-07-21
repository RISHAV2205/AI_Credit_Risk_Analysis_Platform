"""Run validation, feature preparation, and baseline model training."""

from src.components.data_transformation import DataTransformation
from src.components.data_validation import DataValidation
from src.components.model_trainer import ModelTrainer
from src.config.configuration import ConfigurationManager


def main() -> None:
    manager = ConfigurationManager()
    ingestion = manager.get_data_ingestion_config()
    DataValidation(manager.get_data_validation_config()).validate(ingestion.train_data_path, ingestion.test_data_path)
    train_features, test_features = DataTransformation(manager.get_data_transformation_config()).initiate_data_transformation(
        ingestion.train_data_path, ingestion.test_data_path
    )
    ModelTrainer(manager.get_model_trainer_config()).initiate_model_trainer(train_features, test_features)


if __name__ == "__main__":
    main()
