"""Stores and manages application's configuration class"""
import os

from functions.config.files import AppConfig
from functions.config.helpers import get_default_system_config_path
from functions.constants import PACKAGE_BASE_CONFIG_FOLDER


class AppConfigManager:

    """Stores and manages application's configuration files"""

    def __init__(self):
        """Initializes the AppConfigManager class"""
        self.initialize()
        self.app_config = AppConfig.load()

    @property
    def base_dir_path(self) -> str:
        """
        Returns the base directory path for the configuration file
        in relation to a specific system platform like.
        For example, Windows.
        """
        system_config_path = get_default_system_config_path()
        return os.path.join(system_config_path, PACKAGE_BASE_CONFIG_FOLDER)

    def make_base_dir(self) -> None:
        """Creates the base directory for the configuration file"""
        os.makedirs(self.base_dir_path, exist_ok=True)

    def initialize(self):
        """Initializes configuration's scope"""
        self.make_base_dir()
