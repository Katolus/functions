from functions.validators import path_dir_validator
from pathlib import Path
from typing import Any, Dict

from pydantic import BaseModel
from pydantic import ConstrainedStr
from pydantic.dataclasses import dataclass
from pydantic.validators import path_exists_validator
from pydantic.validators import path_validator

from functions.validators import path_has_config_validator


class NotEmptyStr(ConstrainedStr):
    # Make sure that this works for ' '
    strip_whitespace = True
    min_length = 1


class LocalFunctionDir(Path):
    """Validates if a past in directory adhere to the rules"""
    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        field_schema.update(format="functions-path")

    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        yield path_validator
        yield path_exists_validator
        yield path_dir_validator
        yield path_has_config_validator
        yield cls.validate

    @classmethod
    def validate(cls, value: Path) -> Path:
        return value


@dataclass
class DockerImage:
    id: str
    repository: str
    tag: str
    created: str
    size: str


# FunctionConfig
class RunVariables(BaseModel):
    entry_point: str
    name: str
    port: int
    signature_type: str
    source: str


class EnvVariables(BaseModel):
    pass


class DeployVariables(BaseModel):
    allow_unauthenticated: bool = False
    provider: str
    service: str


class FunctionConfig(BaseModel):
    run_variables: RunVariables
    env_variables: EnvVariables
    deploy_variables: DeployVariables
