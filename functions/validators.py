import os
import re
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


def name_validator(v: str) -> str:
    if not re.match("^[a-zA-Z0-9_-]*$", v):
        raise ValueError("Value does not match name requirements")
    return v
