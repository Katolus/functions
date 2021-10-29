from pathlib import Path
from typing import Any, Callable, Dict, Generator, Optional, Type, Union

from pydantic import ConstrainedStr

AnyCallable = Callable[..., Any]
CallableGenerator = Generator[AnyCallable, None, None]
DictStrAny = Dict[str, Any]
NoneBytes = Optional[bytes]
NoneStr = Optional[str]
OptionalInt = Optional[int]
PathStr = Union[Path, str]
StrBytes = Union[str, bytes]

# Used to represent...
ExceptionClass = Type[BaseException]


class NotEmptyStr(ConstrainedStr):
    strip_whitespace: bool = True
    min_length: int = 1
