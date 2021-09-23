"""Stores logic around creating and using a configuration file to amend and enhance the functioning of the package."""
from __future__ import annotations
import os
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List

import toml
from pydantic import BaseModel

BASE_DIR_NAME = "ventress-functions"


class BaseConfig:
    """Base class for the configuration file to enforce a standard interface"""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if not issubclass(value, cls):
            raise ValueError(f"'{value} must of subclassed from {cls}!")
        return value

    def __call__(self, *args: Any, **kwds: Any) -> AppConfig:
        return self()

    def dict(self) -> Dict[str, Any]:
        raise NotImplementedError()


class AppFiles(BaseModel):
    history_file: str = "command_history"
    functions_file: str = "functions_registry"


class AppFunction(BaseModel):
    ...


class AppConfig(BaseModel, BaseConfig):
    default_region: str = ""
    files: AppFiles = AppFiles()
    functions: List[AppFunction] = []


class AppConfigManager(BaseModel):
    """Represents the configuration file for the package"""

    _base_dir: str = BASE_DIR_NAME
    _config_source: str = "config.toml"
    _config: BaseConfig
    config_class: BaseConfig

    def _make_base_dir(self):
        """Create the base directory for the configurations to be stored"""
        # Only on Posix
        os.makedirs(self.base_dir, exist_ok=True)

    def _write(self, file_path: str, content: str):
        with open(file_path, "w") as file:
            file.write(content)

    @property
    def base_dir(self) -> str:
        """Path to the configuration directory."""
        return os.path.join(self.config_home_path, self._base_dir)

    @property
    def config_home_path(self) -> str:
        """Returns the configuration folder"""
        # TODO: Read this from the env first.
        config_folder = ".config"
        return os.path.join(Path().home(), config_folder)

    @property
    def config_path(self) -> str:
        """Returns the path to the configuration file."""
        return os.path.join(self.base_dir, self._config_source)

    @property
    def config_exists(self) -> bool:
        return Path(self.config_path).exists()

    @property
    def config(self):
        if not hasattr(self, "_config") or not self._config:
            self._config = self.config_class()
        return self._config

    def create(self, file_path: str):
        """Create the configuration file if it does not exist."""

        if Path(file_path).exists():
            return

        self._write(file_path, "")

    def read(self) -> Dict[str, Any]:
        """Reads the file config into memory."""
        with open(self.config_path, "r") as file:
            return toml.loads(file.read())

    def load_config(self):
        """Loads the configuration file into the instance."""
        self._make_base_dir()
        if self.config_exists:
            self._config = self.config_class(**self.read())
        else:
            self.create(self.config_path)
            self._config = self.config_class()
            self.save()

    def validate(self):
        """Validate the configuration file before saving"""
        self._config = self.config_class(**self._config.dict())

    def save(self):
        """Saves the current configuration to file."""
        self.validate()
        config_content: str = toml.dumps(self.config.dict())
        self._write(self.config_path, config_content)

    class Config:
        arbitrary_types_allowed = True
        underscore_attrs_are_private = True


app_config = AppConfigManager(config_class=AppConfig)
app_config.load_config()
