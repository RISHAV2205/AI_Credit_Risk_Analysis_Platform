from src.utils.common import read_yaml
from src.constant import CONFIG_FILE_PATH

config = read_yaml(CONFIG_FILE_PATH)

print(config)
print()
print(config.data_ingestion.root_dir)