import os
import sys
from enum import Enum
from enum import unique
from typing import List

# Set system constants based on the current platform
if sys.platform.startswith("win32"):
    DEFAULT_SYSTEM_CONFIG_PATH = os.path.join(os.environ["APPDATA"], "config")
elif sys.platform.startswith("linux"):
    DEFAULT_SYSTEM_CONFIG_PATH = os.path.join(os.environ["HOME"], ".config")
elif sys.platform.startswith("darwin"):
    DEFAULT_SYSTEM_CONFIG_PATH = os.path.join(
        os.environ["HOME"], "Library", "Application Support"
    )
else:
    DEFAULT_SYSTEM_CONFIG_PATH = os.path.join(os.environ["HOME"], "config")

# System configuration
PACKAGE_BASE_CONFIG_FOLDER = "ventress-functions"
PACKAGE_CONFIG_DIR_PATH = os.path.join(
    DEFAULT_SYSTEM_CONFIG_PATH, PACKAGE_BASE_CONFIG_FOLDER
)
DEFAULT_LOG_FILENAME = "functions.log"
DEFAULT_LOG_FILEPATH = os.path.join(PACKAGE_CONFIG_DIR_PATH, DEFAULT_LOG_FILENAME)

# Project constants
PROJECT_VENDOR = "ventress"
PROJECT_MARK = "ventress-functions"


class ConfigName(str, Enum):
    """Represents various availabel names for a config file"""

    BASE = "config.json"


class RequiredFile(str, Enum):
    """Enum for required file names in a function's directory"""

    CONFIG = "config.json"
    DOCKERFILE = "Dockerfile"
    DOCKERIGNORE = ".dockerignore"
    ENTRY_POINT = "main.py"
    REQUIREMENTS = "requirements.txt"


class LoggingLevel(str, Enum):
    DEBUG = "debug"
    ERROR = "error"
    INFO = "info"
    WARNING = "warning"


class FunctionType(str, Enum):
    """Represents the various types of functions that can be run"""

    HTTP = "http"
    PUBSUB = "pubsub"

    @classmethod
    def options(cls) -> List[str]:
        """Returns a list of all the function types"""
        return [enum.value for enum in cls]


class LocalStatus(str, Enum):
    """Represents the status of a function locally"""

    ADDED = "added"
    BUILT = "new build"
    INVALID = "invalid"
    NEW = "new"
    REMOVED = "removed"
    RUNNING = "running"
    STOPPED = "stopped"
    UNKNOWN = "unknown"

    @classmethod
    def build_statuses(cls) -> List[str]:
        """Returns a list of statuses which mean that the image is built"""
        return [
            cls.BUILT,
            cls.RUNNING,
            cls.STOPPED,
        ]


class CloudStatus(str, Enum):
    """Represents the status of a function on the cloud"""

    DELETED = "deleted"
    DEPLOYED = "deployed"
    UNKNOWN = "unknown"

    @property
    def is_deployed(self) -> bool:
        return self == CloudStatus.DEPLOYED


@unique
class CloudProvider(str, Enum):
    """Represents the various cloud providers supported by the functions package"""

    # AWS = "aws"
    # AZURE = "azure"
    GCP = "gcp"
    # LOCAL = "local"
    # OPENFASS = "openfass"
    # OPENSTACK = "openstack"

    @classmethod
    def all(cls) -> List[str]:
        """Returns all the available service types"""
        return [enum.value for enum in cls]


@unique
class CloudServiceType(str, Enum):
    CLOUD_FUNCTION = "cloud_function"

    @classmethod
    def all(cls) -> List[str]:
        """Returns all the available service types"""
        return [enum.value for enum in cls]
