"""Typed configuration and artifact objects used by pipeline stages."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    """All paths and split settings required by the ingestion component."""

    root_dir: Path
    raw_data_path: Path
    train_data_path: Path
    test_data_path: Path
    validation_report_path: Path
    target_column: str
    test_size: float
    random_state: int


@dataclass(frozen=True)
class DataIngestionArtifact:
    """Outputs created by a successful ingestion run."""

    train_data_path: Path
    test_data_path: Path
    validation_report_path: Path


@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    validation_report_path: Path
    target_column: str


@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    preprocessor_path: Path
    train_data_path: Path
    test_data_path: Path
    target_column: str
    identifier_column: str


@dataclass(frozen=True)
class ModelTrainerConfig:
    root_dir: Path
    model_path: Path
    metrics_path: Path
    random_state: int
    C: float
    max_iter: int
    class_weight: str
