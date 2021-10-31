import os
from typing import ClassVar, Optional

from pydantic import BaseModel

from functions.constants import ConfigName
from functions.types import DictStrAny


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
    provider: str
    service: str


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


class FunctionRecord(BaseModel):
    """
    Represents a function record.
    """

    name: str
    config: FunctionConfig

    def __str__(self) -> str:
        return f"{self.name} - {self.config.description}"

    def remove(self) -> None:
        ...


class AppLogging(BaseModel):
    """Represents the logging settings of the application"""

    LOG_FILENAME: ClassVar[str] = "functions.log"
    enabled: bool = False
