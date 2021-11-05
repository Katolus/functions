from __future__ import annotations

import os
from typing import ClassVar, Optional

from pydantic import BaseModel
from pydantic.error_wrappers import ValidationError

from functions import styles
from functions.config.errors import ConfigValidationError
from functions.constants import CloudProvider
from functions.constants import ConfigName
from functions.constants import DEFAULT_LOG_FILE
from functions.constants import FunctionStatus
from functions.constants import FunctionType
from functions.types import DictStrAny
from functions.types import PathStr
from functions.validators import validate_path


class RunVariables(BaseModel):
    """
    RunVariables class.
    """

    # Add some validation to the variables

    entry_point: str
    name: str
    port: int
    signature_type: str
    source: str


class DeployVariables(BaseModel):
    """
    DeployVariables class.
    """

    # Add some validation to the variables

    allow_unauthenticated: Optional[bool]
    provider: CloudProvider
    service: str  # Add supported services
    runtime: str  # Add supported runtimes
    trigger: Optional[str] = None
    region: str


class FunctionConfig(BaseModel):
    """Represents a configuration file of a specific function"""

    path: str
    config_name: ConfigName = ConfigName.BASE
    description: str
    run_variables: RunVariables
    env_variables: DictStrAny
    deploy_variables: DeployVariables

    @property
    def config_path(self) -> str:
        return os.path.join(self.path, self.config_name)

    @classmethod
    def fetch(cls, function_name: str, /) -> FunctionConfig:
        """
        Fetch a function's configuration from the given function name.
        """
        # Consider order of precedence:
        # 1. Config file in the function's directory
        # 2. Config file in the function's registry
        from functions.config.files import FunctionRegistry

        return FunctionRegistry.fetch_function(function_name).config

    @classmethod
    def load(cls, path: PathStr, /) -> FunctionConfig:
        """
        Load a function's configuration from the given path.
        """
        # Validate the path
        valid_path = validate_path(path)

        try:
            # Read the config file
            with open(os.path.join(valid_path, ConfigName.BASE), "r") as config_file:
                # Load as JSON
                config = cls.parse_raw(config_file.read())
        except ValidationError as error:
            raise ConfigValidationError(error=error, path=valid_path)

        # Update the path in config in case changed
        config.path = str(valid_path)
        return config

    @classmethod
    def check_config_file_exists(cls, path: PathStr, /) -> bool:
        """
        Check if the config file exists.
        """
        return os.path.isfile(os.path.join(path, ConfigName.BASE))

    @classmethod
    def load_default_config(cls, function_type: FunctionType, /) -> FunctionConfig:
        """Loads a specific type of a config"""
        if function_type == FunctionType.HTTP:
            # Load the default HTTP config
            ...
            # return Defaults.HTTP.config()

    @classmethod
    def generate(cls, *, type: FunctionType, path: PathStr) -> FunctionConfig:
        """
        Generate a function's configuration file.
        """
        # Validate the path
        valid_path = validate_path(path)

        # Load a default config based on a function type
        config = cls.load_default_config(type)


class FunctionRecord(BaseModel):
    """
    Represents a function record.
    """

    name: str
    config: FunctionConfig
    status: FunctionStatus

    def __str__(self) -> str:
        return " | ".join(
            [
                f"Function - {styles.red(self.name)}",
                f"Local - {styles.blue(self.status.upper())}",
                f"GCP - {styles.blue(self.status.upper())}",
            ]
        )


class AppLogging(BaseModel):
    """Represents the logging settings of the application"""

    LOG_FILENAME: ClassVar[str] = DEFAULT_LOG_FILE
    enabled: bool = False
