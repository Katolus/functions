from __future__ import annotations

from typing import ClassVar, List

from pydantic import BaseModel

from functions.config.models import AppLogging
from functions.config.models import FunctionRecord
from functions.config.types import File
from functions.config.types import TOML
from functions.system import check_if_file_exists
from functions.system import write_to_file


class AppConfig(BaseModel, File, TOML):
    """
    Represents the main configuration file.
    """

    DEFAULT_CONFIG_FILENAME: ClassVar[str] = "config.toml"

    default_region: str = ""
    logging: AppLogging = AppLogging()

    @classmethod
    def write_to_file(cls, content: AppConfig) -> None:
        """Writes a config content to the config file"""
        write_to_file(cls.filepath(), cls.to_toml(content.dict()))

    @classmethod
    def load(cls) -> AppConfig:
        """
        Loads the main configuration from file.
        """
        filepath = cls.filepath()
        if not check_if_file_exists(filepath):
            cls.create()
        return cls.parse_obj(cls.from_toml(filepath))


class FunctionRegistry(BaseModel, File, TOML):
    """
    Represents the function registry file.
    """

    DEFAULT_REGISTRY_FILENAME: str = "registry.toml"
    functions: List[FunctionRecord] = []

    @classmethod
    def write_to_file(cls, content: FunctionRegistry) -> None:
        """Writes a config content to the config file"""
        write_to_file(cls.filepath(), cls.to_toml(content.dict()))

    @classmethod
    def load(cls) -> FunctionRegistry:
        """
        Loads the main configuration from file.
        """
        filepath = cls.filepath()
        if not check_if_file_exists(filepath):
            cls.create()
        return cls.parse_obj(cls.from_toml(filepath))
