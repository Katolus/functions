import os
from pathlib import Path
from typing import Any


from pydantic.errors import PathNotADirectoryError

from functions.errors import ConfigNotFoundError


def path_dir_validator(v: Path) -> Path:
    if not v.is_dir():
        raise PathNotADirectoryError(path=v)

    return v


def path_has_config_validator(v: Any) -> Path:
    if not Path(os.path.join(v, "config.json")).exists():
        raise ConfigNotFoundError(path=v)

    return v


def str_is_alpha_validator(v: str) -> str:
    if not v.isalpha():
        raise ValueError("Not an alphabetic string")
    return v
