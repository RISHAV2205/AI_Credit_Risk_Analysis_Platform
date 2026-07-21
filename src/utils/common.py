import yaml
import json
import joblib

from pathlib import Path
from box import ConfigBox
from ensure import ensure_annotations

from src.logger.logger import logger
from src.exception.exception import CreditRiskException

import sys


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Reads a YAML file and returns its contents as a ConfigBox.

    Args:
        path_to_yaml (Path): Path to the YAML file.

    Returns:
        ConfigBox: YAML content accessible using dot notation.
    """

    try:
        with open(path_to_yaml, "r") as yaml_file:
            content = yaml.safe_load(yaml_file)   #safeload convert to pyhton dict

            logger.info(f"YAML file loaded successfully: {path_to_yaml}")

            return ConfigBox(content)

    except Exception as e:
        logger.error(f"Failed to read YAML file: {path_to_yaml}")

        raise CreditRiskException(e, sys)
    
    
@ensure_annotations
def create_directories(
    path_to_directories: list,
    verbose: bool = True,
):
    """
    Create directories if they don't already exist.

    Args:
        path_to_directories (list): List of directory paths.
        verbose (bool): Whether to log directory creation.
    Why use parents=True?
    Because intermediate directories may not exist, and we want Python to create the complete directory tree automatically.
    """

    try:
        for path in path_to_directories:

            Path(path).mkdir(
                parents=True,
                exist_ok=True
            )

            if verbose:
                logger.info(f"Created directory at: {path}")

    except Exception as e:
        raise CreditRiskException(e, sys)
    
@ensure_annotations
def save_json(path: Path, data: dict):
    """
    Save a dictionary as a JSON file.

    Args:
        path (Path): Output JSON file path.
        data (dict): Dictionary to save.
    """

    try:
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w") as f:
            json.dump(data, f, indent=4)

        logger.info(f"JSON file saved at: {path}")

    except Exception as e:
        raise CreditRiskException(e, sys)
    
    
    
@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """
    Load a JSON file and return its contents as a ConfigBox.

    Args:
        path (Path): Path to the JSON file.

    Returns:
        ConfigBox: JSON content with dot notation support.
    """

    try:
        with open(path, "r") as f:
            content = json.load(f)

        logger.info(f"JSON file loaded successfully from: {path}")

        return ConfigBox(content)

    except Exception as e:
        logger.error(f"Failed to load JSON file: {path}")
        raise CreditRiskException(e, sys)
    
@ensure_annotations
def save_pickle(path: Path, obj: object):
    """
    Save any Python object as a pickle file.
    Args:
        path (Path): Output file path.
        obj (object): Python object to save.
    """

    try:
        path.parent.mkdir(parents=True, exist_ok=True)

        joblib.dump(obj, path)

        logger.info(f"Pickle file saved at: {path}")

    except Exception as e:
        raise CreditRiskException(e, sys)
    
@ensure_annotations
def load_pickle(path: Path):
    """
    Load a Python object from a pickle file.
    Args:
        path (Path): Pickle file path.

    Returns:
        object: Loaded Python object.
    """
    try:
        obj = joblib.load(path)
        logger.info(f"Pickle file loaded successfully from: {path}")
        return obj
    except Exception as e:
        raise CreditRiskException(e, sys)