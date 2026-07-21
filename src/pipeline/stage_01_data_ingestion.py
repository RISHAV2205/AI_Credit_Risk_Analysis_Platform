"""Runnable entry point for the first pipeline stage."""

from src.components.data_ingestion import DataIngestion
from src.config.configuration import ConfigurationManager
from src.logger.logger import logger


def main() -> None:
    config_manager = ConfigurationManager()
    ingestion_config = config_manager.get_data_ingestion_config()
    artifact = DataIngestion(ingestion_config, config_manager.schema).initiate_data_ingestion()
    logger.info("Train data saved to %s", artifact.train_data_path)
    logger.info("Test data saved to %s", artifact.test_data_path)
    logger.info("Validation report saved to %s", artifact.validation_report_path)


if __name__ == "__main__":
    main()
