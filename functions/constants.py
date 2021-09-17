from enum import Enum

class ConfigName(str, Enum):
    BASE = "config.json"



class DockerLabel(str, Enum):
    """Stores constants under which variables are stored"""
    CONFIG: str = "package.functions.config"
    CONFIG_PATH: str = "package.functions.config_path"
    FUNCTION_NAME: str = "package.functions.function_name"
    FUNCTION_PATH: str = "package.functions.function_path"
    ORGANISATION: str = "package.functions.organisation"


