from enum import Enum
from enum import unique


@unique
class DockerLabel(str, Enum):
    """Stores constants under which variables are stored"""

    CONFIG = "package.functions.config"
    CONFIG_PATH = "package.functions.config_path"
    FUNCTION_NAME = "package.functions.function_name"
    FUNCTION_PATH = "package.functions.function_path"
    ORGANISATION = "package.functions.organisation"
