from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel

from functions import logs
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

        logs.debug(f"Writing function registry to file: {cls.filepath()}")
        write_to_file(cls.filepath(), cls.to_toml(content.dict()))

    @classmethod
    def load(cls) -> AppConfig:
        """Loads the main configuration from file"""
        filepath = cls.filepath()
        if not check_if_file_exists(filepath):
            logs.debug(f"Config file not found: {filepath}")
            cls.create()
            logs.debug(f"Config file created: {filepath}")
        return cls.parse_obj(cls.from_toml(filepath))


class FunctionRegistry(BaseModel, File):
    """Represents the function registry file"""

    DEFAULT_FILENAME: ClassVar[str] = "registry.json"
    functions: FunctionsMap = {}

    @classmethod
    def write_to_file(cls, content: FunctionRegistry) -> None:
        """Writes a config content to the config file"""

        logs.debug(f"Writing function registry to file: {cls.filepath()}")
        write_to_file(cls.filepath(), content.json())

    @classmethod
    def load(cls) -> FunctionRegistry:
        """Loads the main configuration from file"""

        filepath = cls.filepath()
        if not check_if_file_exists(filepath):
            cls.create()
        return cls.parse_file(filepath)

    @classmethod
    def check_if_function_in_registry(cls, function_name: str) -> bool:
        """Checks if a function is in the registry"""
        return function_name in cls.load().functions

    @classmethod
    def fetch_function(cls, function_name: str) -> FunctionRecord:
        """Returns the function record for a function"""
        return cls.load().functions[function_name]

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
        logs.debug(f"Added function {function.name} to registry")

    @classmethod
    def update_function(cls, function: FunctionRecord) -> None:
        """Updates a function in the registry"""

        registry = cls.load()
        # Check if the function already exists
        if function.name not in registry.functions:
            # Swap with a custom error class
            raise ValueError(
                f"Function {function.name} does not exist in the registry."
            )
        registry.functions[function.name] = function
        registry.write_to_file(registry)
        logs.debug(f"Updated function {function.name} in registry")

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
        logs.debug(f"Removed function {function_name} from registry")
