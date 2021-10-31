"""Stores and manages application's configuration class"""
import os

from functions.config import AppConfig
from functions.config.constants import PACKAGE_BASE_CONFIG_FOLDER
from functions.config.helpers import get_default_system_config_path
from functions.system import check_if_file_exists
from functions.system import write_to_file


class AppConfigManager:
    DEFAULT_CONFIG_FILENAME: str = "config.toml"

    """Stores and manages application's configuration files"""

    def __init__(self, config_filename=None):
        """Initializes the AppConfigManager class"""
        self.config_filename = config_filename or self.DEFAULT_CONFIG_FILENAME
        self.config: AppConfig = {}
        self.initialize_config()

    @property
    def base_dir_path(self) -> str:
        """
        Returns the base directory path for the configuration file
        considering a specific system platform like. For example, Windows.
        """
        system_config_path = get_default_system_config_path()
        return os.path.join(
            system_config_path, PACKAGE_BASE_CONFIG_FOLDER, self.config_filename
        )

    @property
    def config_filepath(self) -> str:
        """Returns the configuration file path"""
        return os.path.join(self.base_dir_path, self.config_filename)

    def default_config(self) -> AppConfig:
        """Returns the default configuration for the application"""
        raise NotImplementedError

    def make_base_dir(self) -> None:
        """Creates the base directory for the configuration file"""
        os.makedirs(self.base_dir_path, exist_ok=True)

    def initialize_config(self):
        """Initializes the configuration file"""
        if check_if_file_exists(self.config_filepath):
            self.load_config()
        else:
            self.create_config()

    def write_to_config(self, config: AppConfig) -> None:
        """Writes the configuration into the configuration file"""
        write_to_file(self.config_filepath, config.to_toml())

    def save_config(self) -> None:
        """Saves the configuration into the configuration file"""
        write_to_file(self.config_filepath, self.config.to_toml())

    def create_config(self) -> None:
        """Creates the main configuration file"""
        self.make_base_dir()
        # Write default configuration into the config file
        self.write_to_config(self.default_config)

    def load_config(self) -> None:
        """Loads the configuration from the configuration file"""
        self.config = AppConfig.from_toml(self.config_filepath)
