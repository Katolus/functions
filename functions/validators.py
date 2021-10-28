import os
import re
from pathlib import Path
from typing import Any

from functions.constants import ConfigName
from functions.errors import ConfigNotFoundError
from functions.errors import PathNotADirectoryError
from functions.types import PathStr


def path_dir_validator(v: PathStr) -> PathStr:
    if not Path(v).is_dir():
        raise PathNotADirectoryError(path=v)

    return v


def path_includes_config_validator(v: Any) -> Path:
    if not Path(os.path.join(v, ConfigName.BASE)).exists():
        raise ConfigNotFoundError(path=v)

    return v


def name_validator(v: str) -> str:
    if not re.match("^[a-zA-Z0-9_-]*$", v):
        raise ValueError("Value does not match name requirements")
    return v


def validate_path(v: PathStr) -> Path:
    """Validates if a path is a valid directory"""
    path_dir_validator(v)
    path_includes_config_validator(v)
    return Path(v)
