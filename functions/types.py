import os
from pathlib import Path
from pathlib import _windows_flavour, _posix_flavour
from typing import Any, Callable, Dict, Generator, Optional, Type, Union

from pydantic import ConstrainedStr
from pydantic.validators import path_exists_validator
from pydantic.validators import path_validator

from functions.validators import path_dir_validator
from functions.validators import path_has_config_validator


AnyCallable = Callable[..., Any]
CallableGenerator = Generator[AnyCallable, None, None]
NoneBytes = Optional[bytes]
NoneStr = Optional[str]
OptionalInt = Optional[int]
DictStrAny = Dict[str, Any]
StrBytes = Union[str, bytes]

ExceptionClass = Type[BaseException]

class NotEmptyStr(ConstrainedStr):
    # TODO: Make sure that this works for ' '
    strip_whitespace: bool = True
    min_length: int = 1


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
