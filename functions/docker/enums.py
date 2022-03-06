from enum import Enum
from enum import unique


@unique
class DockerLabel(str, Enum):
    """Stores constants under which variables are stored"""

    CONFIG_CONTENT = "org.ventress.functions.image.config.content"
    CONFIG_PATH = "org.ventress.functions.image.config.path"
    DESCRIPTION = "org.ventress.functions.image.description"
    FUNCTION_NAME = "org.ventress.functions.image.name"
    FUNCTION_SOURCE = "org.ventress.functions.image.source"
    MARK = "org.ventress.functions.image.mark"
    VENDOR = "org.ventress.functions.image.vendor"
    VERSION = "org.ventress.functions.image.version"
