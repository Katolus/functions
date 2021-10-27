import os
from pathlib import Path
from enum import Enum
from enum import unique
from typing import List

# Configration
BASE_DIR_NAME = "ventress-functions"
CONFIG_FOLDER_NAME = ".config"  # Set based on environment
APP_CONFIG_PATH = os.path.join(
    str(Path().home()),
    CONFIG_FOLDER_NAME,
    BASE_DIR_NAME,
)


class ConfigName(str, Enum):
    """Represents various availabel names for a config file"""

    BASE = "config.json"


class SignatureType(str, Enum):
    PUBSUB = "event"
    HTTP = "http"


class DockerLabel(str, Enum):
    """Stores constants under which variables are stored"""

    CONFIG: str = "package.functions.config"
    CONFIG_PATH: str = "package.functions.config_path"
    FUNCTION_NAME: str = "package.functions.function_name"
    FUNCTION_PATH: str = "package.functions.function_path"
    ORGANISATION: str = "package.functions.organisation"


class LoggingLevel(str, Enum):
    DEBUG = "debug"
    ERROR = "error"
    INFO = "info"
    WARNING = "warning"


@unique
class CloudServiceType(str, Enum):
    CLOUD_FUNCTION = "cloud_function"

    @classmethod
    def all(cls) -> List[str]:
        """Returns all the available service types"""
        return [enum.value for enum in cls]
