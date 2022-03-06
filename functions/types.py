from pathlib import Path
from typing import Any, Callable, Dict, Generator, Optional, Type, Union

AnyCallableT = Callable[..., Any]
CallableGenerator = Generator[AnyCallableT, None, None]
DictStrAny = Dict[str, Any]
NoneBytes = Optional[bytes]
NoneStr = Optional[str]
OptionalInt = Optional[int]
PathStr = Union[Path, str]
StrBytes = Union[str, bytes]

# Used to represent...
ExceptionClass = Type[BaseException]
