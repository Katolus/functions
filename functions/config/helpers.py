import os
import sys

from functions.constants import PACKAGE_BASE_CONFIG_FOLDER


def get_default_system_config_path():
    """
    Return a system's default path for storing app configurations.
    """
    # Copilot generated - Validate in actions
    # Assumes that env keys are present in a system's environment
    if sys.platform.startswith("win32"):
        return os.path.join(os.environ["APPDATA"], "config")
    elif sys.platform.startswith("linux"):
        return os.path.join(os.environ["HOME"], ".config")
    elif sys.platform.startswith("darwin"):
        return os.path.join(os.environ["HOME"], "Library", "Application Support")
    else:
        return os.path.join(os.environ["HOME"], "config")


def construct_filepath_in_config(filename: str) -> str:
    """
    Construct a config filepath based on the system's default config path.
    """
    return os.path.join(
        get_default_system_config_path(), PACKAGE_BASE_CONFIG_FOLDER, filename
    )
