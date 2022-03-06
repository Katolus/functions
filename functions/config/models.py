from __future__ import annotations

import json
import os
from pathlib import Path
from typing import ClassVar, Optional

from pydantic import BaseModel
from pydantic.error_wrappers import ValidationError

from functions import logs
from functions import styles
from functions.config.enums import FunctionConfigVersion
from functions.config.errors import ConfigValidationError
from functions.config.errors import InvalidFunctionSource
from functions.constants import CloudProvider
from functions.constants import CloudServiceType
from functions.constants import CloudStatus
from functions.constants import ConfigName
from functions.constants import DEFAULT_LOG_FILENAME
from functions.constants import FunctionType
from functions.constants import LocalStatus
from functions.errors import InvalidFunctionTypeError
from functions.types import DictStrAny
from functions.types import PathStr
from functions.validators import validate_name
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
    region: str
    runtime: str  # Add supported runtimes
    service: str  # Add supported services
    trigger_value: Optional[str] = None
    trigger: Optional[str] = None


class FunctionConfig(BaseModel):
    """Represents a configuration file of a specific function"""

    config_name: ConfigName = ConfigName.BASE
    config_version: FunctionConfigVersion = FunctionConfigVersion.latest()
    deploy_variables: DeployVariables
    description: str
    env_variables: DictStrAny
    path: str
    run_variables: RunVariables

    def __init__(self, **data: DictStrAny) -> None:
        """Initialize function's config file from path or from data"""
        # We accept the file to be the first source of truth
        # If the path is not provided, we use the data as the second source of truth

        # Check if config at path still exists
        path: str = data.get("path")
        if Path(path).exists() and Path(os.path.join(path, ConfigName.BASE)).is_file():
            # Load the config file data instead
            with open(os.path.join(path, ConfigName.BASE), "r") as config_file:
                # Load file as JSON format
                json_data = json.loads(config_file.read())

                # Initiate the class with the loaded data
                super().__init__(**json_data)
                logs.debug(
                    f"Loaded config file ({self.run_variables.name}) from path: {path}"
                )
                return None

        super().__init__(**data)
        logs.debug(f"Loaded config file ({self.run_variables.name}) from registry")
        return None

    @property
    def config_path(self) -> str:
        return str(os.path.join(self.path, self.config_name))

    def is_source_valid(self) -> bool:
        """
        Checks if the function's source is valid
        """
        # Check if the source is valid
        if not self.path:
            return False

        # Check if the source exists
        if not Path(self.path).exists():
            return False

        return True

    def validate_source(self) -> None:
        """
        Validate the function's source.
        """
        # Check if the source is valid
        if not self.is_source_valid():
            raise InvalidFunctionSource(
                f_name=self.run_variables.name, source=self.path
            )

    def save(self) -> None:
        """
        Store the function config file in the given path.
        """
        from functions.system import write_to_file

        write_to_file(os.path.join(self.path, ConfigName.BASE), self.json())

    @classmethod
    def default(
        cls,
        cloud_provider: CloudProvider,
        cloud_service_type: CloudServiceType,
        function_dir: str,
        function_name: str,
        port: int,
        region: str,
        runtime: str,
        signature_type: str,
        trigger: str,
        trigger_value: str = None,
    ) -> FunctionConfig:
        """Returns a instance of class with some default values"""
        validate_name(function_name)

        return cls.parse_obj(
            {
                "description": str(
                    f"Default functions template generated for '{function_name}' of '{signature_type}' type",
                ),
                "path": function_dir,
                "run_variables": {
                    "entry_point": "main",
                    "name": function_name,
                    "port": port,
                    "signature_type": signature_type,
                    "source": "main.py",
                },
                "env_variables": {},
                "deploy_variables": {
                    "provider": cloud_provider,
                    "region": region,
                    "runtime": runtime,
                    "service": cloud_service_type,
                    "trigger": trigger,
                    "trigger_value": trigger_value,
                },
            }
        )

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
    def load_default_config(
        cls, f_name: str, f_type: FunctionType, f_path: PathStr, /
    ) -> FunctionConfig:
        """Loads a specific type of a config"""
        from functions.defaults import Defaults

        if f_type == FunctionType.HTTP:
            # Load the default HTTP config
            return Defaults.GCP.CloudFunction.HTTP.config(f_name, f_path)
        if f_type == FunctionType.PUBSUB:
            # Load the default PUBSUB config
            return Defaults.GCP.CloudFunction.PubSub.config(f_name, f_path)
        raise InvalidFunctionTypeError(type=f_type)

    @classmethod
    def generate(
        cls, f_name: str, f_type: FunctionType, f_path: PathStr, /
    ) -> FunctionConfig:
        """
        Generate a function's configuration file.
        """
        # Load a default config based on a function type
        return cls.load_default_config(f_name, f_type, f_path)


class FunctionStatus(BaseModel):
    """A class representing the status of a function"""

    LOCAL: LocalStatus = LocalStatus.UNKNOWN
    GCP: CloudStatus = CloudStatus.UNKNOWN


class FunctionRecord(BaseModel):
    """
    Represents a function record.
    """

    name: str
    config: FunctionConfig
    status: FunctionStatus = FunctionStatus()

    def __str__(self) -> str:
        message_chunks = [
            f"Function - {styles.red(self.name)}",
        ]
        if self.status.LOCAL:
            message_chunks.append(
                f"Local - {styles.blue(self.status.LOCAL.upper())}",
            )

        if self.status.GCP:
            message_chunks.append(
                f"GCP - {styles.blue(self.status.GCP.upper())}",
            )

        return " | ".join(message_chunks)

    def set_local_status(self, status: LocalStatus) -> None:
        """
        Set the local status of the function.
        """
        self.status.LOCAL = status

    def set_gcp_status(self, status: CloudStatus) -> None:
        """
        Set the GCP status of the function.
        """
        self.status.GCP = status

    def update_registry(self) -> None:
        """
        Update the function registry with the current function record.
        """
        from functions.config.files import FunctionRegistry

        FunctionRegistry.store_function(self)


class AppLogging(BaseModel):
    """Represents the logging settings of the application"""

    LOG_FILENAME: ClassVar[str] = DEFAULT_LOG_FILENAME
    enabled: bool = False
