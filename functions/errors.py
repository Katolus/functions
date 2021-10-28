from typing import Any

from pydantic import PydanticValueError

from functions.mixins import FunctionErrorMixin
from functions.types import CallableGenerator
from functions.types import PathStr


class FunctionBaseError(FunctionErrorMixin, Exception):
    # Pydantic
    @classmethod
    def __get_validators__(cls) -> CallableGenerator:
        yield cls.validate

    @classmethod
    def validate(cls, value: Any) -> Any:
        # if not issubclass(value, cls):
        #     raise ConfigError(f"'{value}'Is not a valid exception class")
        return value


class _DerivedError(FunctionBaseError):
    def __init__(self, *, error: Exception) -> None:
        super().__init__(error=error)


class _PathValueError(PydanticValueError):
    def __init__(self, *, path: PathStr) -> None:
        super().__init__(path=str(path))


class IsNotAValidDirectory(_PathValueError, FunctionBaseError):
    code = "path.invalid_directory"
    msg_template = "Path '{path}' is not a valid function directory"


class ConfigNotFoundError(_PathValueError, FunctionBaseError):
    code = "path.config_not_found"
    msg_template = "Path '{path}' does not include a valid config file"


class PathNotADirectoryError(_PathValueError):
    code = "path.not_a_directory"
    msg_template = 'Path "{path}" does not point to a directory'


class FunctionBuildError(_DerivedError):
    code = "build.error"
    msg_template = "Function build has field with the following error -> {error}"


class ConfigValidationError(_DerivedError):
    code = "config.validation"
    msg_template = "Config file validation failed with error -> {error}"


class FunctionNameTaken(FunctionBaseError):
    code = "functions.name_taken"
    msg_template = "Function with that name ('{name}') already exists"

    def __init__(self, name: str, /) -> None:
        super().__init__(name=name)
