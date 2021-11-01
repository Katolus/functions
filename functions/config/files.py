from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel

from functions.config.interfaces import File
from functions.config.interfaces import TOML
from functions.config.models import AppLogging
from functions.config.models import FunctionRecord
from functions.config.types import FunctionsMap
from functions.system import check_if_file_exists
from functions.system import write_to_file


class AppConfig(BaseModel, File, TOML):
    """Represents the main configuration file"""

    DEFAULT_FILENAME: ClassVar[str] = "config.toml"

    default_region: str = ""
    logging: AppLogging = AppLogging()

    @classmethod
    def write_to_file(cls, content: AppConfig) -> None:
        """Writes a config content to the config file"""
        write_to_file(cls.filepath(), cls.to_toml(content.dict()))

    @classmethod
    def load(cls) -> AppConfig:
        """Loads the main configuration from file"""
        filepath = cls.filepath()
        if not check_if_file_exists(filepath):
            cls.create()
        return cls.parse_obj(cls.from_toml(filepath))


class FunctionRegistry(BaseModel, File, TOML):
    """Represents the function registry file"""

    DEFAULT_FILENAME: ClassVar[str] = "registry.toml"
    functions: FunctionsMap = {}

    @classmethod
    def write_to_file(cls, content: FunctionRegistry) -> None:
        """Writes a config content to the config file"""

        write_to_file(cls.filepath(), cls.to_toml(content.dict()))

    @classmethod
    def load(cls) -> FunctionRegistry:
        """Loads the main configuration from file"""

        filepath = cls.filepath()
        if not check_if_file_exists(filepath):
            cls.create()
        return cls.parse_obj(cls.from_toml(filepath))

    @classmethod
    def add_function(cls, function: FunctionRecord) -> None:
        """Adds a function to the registry"""

        registry = cls.load()
        # Check if the function already exists
        if function.name in registry.functions:
            # Swap with a custom error class
            raise ValueError(
                f"Function {function.name} already exists in the registry."
            )
        registry.functions[function.name] = function
        registry.write_to_file(registry)

    @classmethod
    def remove_function(cls, function_name: str) -> None:
        """Removes a function from the registry"""

        registry = cls.load()
        if function_name not in registry.functions:
            raise ValueError(
                f"Function {function_name} does not exist in the registry."
            )
        del registry.functions[function_name]
        registry.write_to_file(registry)
