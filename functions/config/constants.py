from functions import __version__

from .enums import AppConfigVersion

APP_CONFIG_VERSION_MAP = {
    "0.1.0a3": AppConfigVersion.V1.value,
}

# Get config version matching the package version or default to the latest
APP_CONFIG_VERSION = (
    APP_CONFIG_VERSION_MAP.get(__version__) or AppConfigVersion.latest().value
)
