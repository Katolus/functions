from enum import Enum
from typing import List

class ConfigName(str, Enum):
    BASE = "config.json"



class DockerLabel(str, Enum):
    """Stores constants under which variables are stored"""
    CONFIG: str = "package.functions.config"
    CONFIG_PATH: str = "package.functions.config_path"
    FUNCTION_NAME: str = "package.functions.function_name"
    FUNCTION_PATH: str = "package.functions.function_path"
    ORGANISATION: str = "package.functions.organisation"


class CloudServiceType(str, Enum):
    CLOUD_FUNCTION = "cloud_function"

    @classmethod
    def all(cls) -> List[str]:
        # TODO: There might be a method that does this better
        return [cls.CLOUD_FUNCTION]
