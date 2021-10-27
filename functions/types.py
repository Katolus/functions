from typing import Any, Callable, Dict, Generator, Optional, Type, Union

from pydantic import ConstrainedStr

AnyCallable = Callable[..., Any]
CallableGenerator = Generator[AnyCallable, None, None]
NoneBytes = Optional[bytes]
NoneStr = Optional[str]
OptionalInt = Optional[int]
DictStrAny = Dict[str, Any]
StrBytes = Union[str, bytes]

ExceptionClass = Type[BaseException]


class NotEmptyStr(ConstrainedStr):
    strip_whitespace: bool = True
    min_length: int = 1
