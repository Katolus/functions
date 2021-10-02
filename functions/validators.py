import os
import re
from pathlib import _windows_flavour, _posix_flavour
from pathlib import Path
from typing import Any

from pydantic.errors import PathNotADirectoryError
from pydantic.validators import path_exists_validator
from pydantic.validators import path_validator

from functions.errors import ConfigNotFoundError
from functions.types import CallableGenerator


def path_dir_validator(v: Path) -> Path:
    if not v.is_dir():
        raise PathNotADirectoryError(path=v)

    return v


def path_has_config_validator(v: Any) -> Path:
    if not Path(os.path.join(v, "config.json")).exists():
        raise ConfigNotFoundError(path=v)

    return v


def name_validator(v: str) -> str:
    if not re.match("^[a-zA-Z0-9_-]*$", v):
        raise ValueError("Value does not match name requirements")
    return v


class LocalFunctionPath(Path):
    """Validates if a past in directory adhere to the rules"""

    # Questionable
    _flavour = _windows_flavour if os.name == "nt" else _posix_flavour

    @classmethod
    def __get_validators__(cls) -> CallableGenerator:
        yield path_validator
        yield path_exists_validator
        yield path_dir_validator
        yield path_has_config_validator
        yield cls.validate

    @classmethod
    def validate(cls, value: Path) -> Path:
        return value
