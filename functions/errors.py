from pathlib import Path
from typing import Any

from pydantic import PydanticValueError

from functions.mixins import FunctionErrorMixin


class FunctionBaseError(FunctionErrorMixin, Exception):
    # Pydantic
    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        yield cls.validate

    @classmethod
    def validate(cls, value: Any) -> Any:
        # TODO: Think about enhancing this validation if it is going to be enforced
        # if not issubclass(value, cls):
        #     raise ConfigError(f"'{value}'Is not a valid exception class")
        return value



class FunctionValueError(PydanticValueError, FunctionBaseError):
    ...


class _PathValueError(PydanticValueError):
    def __init__(self, *, path: Path) -> None:
        super().__init__(path=str(path))


class IsNotAValidDirectory(_PathValueError, FunctionBaseError):
    code = "path.invalid_directory"
    msg_template = "path '{path}' is not a valid function directory"


class ConfigNotFoundError(_PathValueError, FunctionBaseError):
    code = "path.config_not_found"
    msg_template = "path '{path}' does not include a valid config file"
