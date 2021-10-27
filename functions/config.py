"""Stores logic around creating and using a configuration file to amend and enhance the functioning of the package."""
from __future__ import annotations
import os
from pathlib import Path
from typing import Any, Optional
from typing import Dict
from typing import List
from typing import Type

import toml  # type: ignore
from pydantic import BaseModel
from functions.constants import ConfigName

from functions.constants import BASE_DIR_NAME
from functions.types import CallableGenerator


class BaseConfig:
    """Base class for the configuration file to enforce a standard interface"""

    @classmethod
    def __get_validators__(cls) -> CallableGenerator:
        yield cls.validate

    @classmethod
    def validate(cls, value: Type[BaseConfig]) -> Type[BaseConfig]:
        if not issubclass(value, cls):
            raise ValueError(f"'{value} must of subclassed from {cls}!")
        return value

    def __call__(self) -> BaseConfig:
        return self()

    def dict(self) -> Dict[str, Any]:
        raise NotImplementedError()


class AppFiles(BaseModel):
    """Represents the names of files the relate to this application"""

    history_file: str = "command_history"
    functions_file: str = "functions_registry"


class AppLogging(BaseModel):
    """Represents the logging settings of the application"""

    is_logging: bool = False  # Look into making the logging
    logging_file: str = "functions.log"


class AppFunction(BaseModel):
    """Stores a configuration of a specific funcion"""

    name: str
    config: FunctionConfig


class AppConfig(BaseModel, BaseConfig):
    """Holds all the variables for the config file"""

    default_region: str = ""
    files: AppFiles = AppFiles()
    functions: List[AppFunction] = []
    logging: AppLogging = AppLogging()


class AppConfigManager(BaseModel):
    """Represents the configuration file for the package"""

    _base_dir: str = BASE_DIR_NAME
    _config_source: str = "config.toml"
    _config: BaseConfig
    config_class: Type[BaseConfig]

    def _make_base_dir(self) -> None:
        """Create the base directory for the configurations to be stored"""
        # Only on Posix
        os.makedirs(self.base_dir, exist_ok=True)

    def _write(self, file_path: str, content: str) -> None:
        with open(file_path, "w") as file:
            file.write(content)

    @property
    def base_dir(self) -> str:
        """Path to the configuration directory."""
        return os.path.join(self.config_home_path, self._base_dir)

    @property
    def config_home_path(self) -> str:
        """Returns the configuration folder"""
        # Read this from the env first.
        config_folder = ".config"
        return os.path.join(str(Path().home()), config_folder)

    @property
    def config_path(self) -> str:
        """Returns the path to the configuration file."""
        return os.path.join(self.base_dir, self._config_source)

    @property
    def config_exists(self) -> bool:
        return Path(self.config_path).exists()

    @property
    def config(self) -> BaseConfig:
        if not hasattr(self, "_config") or not self._config:
            self._config = self.config_class()
        return self._config


    def create(self, file_path: str) -> None:
        """Create the configuration file if it does not exist."""

        if Path(file_path).exists():
            return

        self._write(file_path, "")

    def read(self) -> Dict[str, Any]:
        """Reads the file config into memory."""
        with open(self.config_path, "r") as file:
            return toml.loads(file.read())

    def load_config(self) -> None:
        """Loads the configuration file into the instance."""
        self._make_base_dir()
        if self.config_exists:
            self._config = self.config_class(**self.read())
        else:
            self.create(self.config_path)
            self._config = self.config_class()
            self.save()

    def verify(self) -> None:
        """Validate the configuration file before saving"""
        self._config = self.config_class(**self._config.dict())

    def save(self) -> None:
        """Saves the current configuration to file."""
        self.verify()
        config_content: str = toml.dumps(self.config.dict())
        self._write(self.config_path, config_content)

    class Config:
        arbitrary_types_allowed = True
        underscore_attrs_are_private = True


def config_dir() -> str:
    """Returns a directory path to were the configuration file is stored."""
    return AppConfigManager().config_home_path


app_config = AppConfigManager(config_class=AppConfig)
app_config.load_config()


# FunctionConfig
class RunVariables(BaseModel):
    """Holds the run time variables"""

    entry_point: str
    name: str
    port: int
    signature_type: str
    source: str


class EnvVariables(Dict[str, str]):
    """Holds environmental variables"""

    ...


class DeployVariables(BaseModel):
    """Holds deploy specific variables"""

    allow_unauthenticated: Optional[bool]
    provider: str
    service: str


class FunctionConfig(BaseModel):
    """Represents a configuration file of a specific function"""

    path: str
    config_name: ConfigName = ConfigName.BASE
    description: str
    run_variables: RunVariables
    env_variables: EnvVariables
    deploy_variables: DeployVariables

    @property
    def config_path(self) -> str:
        return os.path.join(self.path, self.config_name)
