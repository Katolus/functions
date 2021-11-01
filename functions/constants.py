from enum import Enum
from enum import unique
from typing import List

PACKAGE_BASE_CONFIG_FOLDER = "ventress-functions"
DEFAULT_LOG_FILE = "functions.log"


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


class FunctionStatus(str, Enum):
    """Represents the status of a function"""

    BUILT = "built"
    CREATED = "created"
    DEPLOYED = "deployed"
    RUNNING = "running"
    STOPPED = "stopped"
    UNKNOWN = "unknown"


@unique
class CloudServiceType(str, Enum):
    CLOUD_FUNCTION = "cloud_function"

    @classmethod
    def all(cls) -> List[str]:
        """Returns all the available service types"""
        return [enum.value for enum in cls]
