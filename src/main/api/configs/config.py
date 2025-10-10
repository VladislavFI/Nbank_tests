from pathlib import Path
from typing import Any

class Config:
    _instance = None
    _properties = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            config_path = Path(__file__).parents[3] / 'resources' / 'config.properties'
            if not config_path.exists():
                raise ImportError(f'{config_path}: config.properties not found')
            with open(config_path, 'r') as f:
                for line in f:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        cls._properties[key.strip()] = value.strip()
        return cls._instance

    @staticmethod
    def get(key: str, default_value: Any = None) -> Any:
        # Ensure the config is loaded
        _ = Config()
        return Config._properties.get(key, default_value)