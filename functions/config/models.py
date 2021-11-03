from __future__ import annotations

import os
from typing import ClassVar, Optional

from pydantic import BaseModel
from pydantic.decorator import validate_arguments
from pydantic.error_wrappers import ValidationError

from functions import styles
from functions.config.errors import ConfigValidationError
from functions.constants import CloudProvider
from functions.constants import ConfigName
from functions.constants import DEFAULT_LOG_FILE
from functions.constants import FunctionStatus
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

        return FunctionRegistry.get_function_record(function_name).config

    @classmethod
    @validate_arguments
    def load(cls, path: PathStr, /) -> FunctionConfig:
        """
        Load a function's configuration from the given path.
        """
        # Validate the path
        valid_path = validate_path(path)

        try:
            # Read the config file
            with open(valid_path, "r") as config_file:
                # Load as JSON
                config = cls.parse_raw(config_file.read())
        except ValidationError as error:
            raise ConfigValidationError(error=error, path=valid_path)

        # Update the path in config in case changed
        config.path = os.path.dirname(valid_path)
        return config


class FunctionRecord(BaseModel):
    """
    Represents a function record.
    """

    name: str
    config: FunctionConfig
    status: FunctionStatus

    def __str__(self) -> str:
        return (
            f"Function - {styles.red(self.name)}"
            f" | Status - {styles.blue(self.status)}"
        )


class AppLogging(BaseModel):
    """Represents the logging settings of the application"""

    LOG_FILENAME: ClassVar[str] = DEFAULT_LOG_FILE
    enabled: bool = False
