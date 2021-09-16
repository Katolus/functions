from pathlib import Path
from typing import Any

from pydantic import PydanticValueError

from functions.mixins import ValidatorMixin
from functions.mixins import FunctionErrorMixin


class FunctionBaseError(FunctionErrorMixin, ValidatorMixin, Exception):
    ...


class FunctionValueError(PydanticValueError, FunctionBaseError):
    ...


class _PathValueError(PydanticValueError):
    def __init__(self, *, path: Path) -> None:
        super().__init__(path=str(path))


class ItIsNotAValidDirectory(_PathValueError, FunctionBaseError):
    code = "path.invalid_directory"
    msg_template = "path '{path}' is not a valid function directory"


class ConfigNotFoundError(_PathValueError, FunctionBaseError):
    code = "code.config_not_found"
    msg_template = "path '{path}' does not include a valid config file"
