from pathlib import Path

# ----------------------------------------------------------
# Project Root Directory
# ----------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# ----------------------------------------------------------
# Configuration Files
# ----------------------------------------------------------

CONFIG_FILE_PATH = PROJECT_ROOT / "config" / "config.yaml"

PARAMS_FILE_PATH = PROJECT_ROOT / "config" / "params.yaml"

SCHEMA_FILE_PATH = PROJECT_ROOT / "config" / "schema.yaml"