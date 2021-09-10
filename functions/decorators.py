from functools import wraps
from typing import Any, Callable, Optional

AnyCallableT = Callable[..., Any]


def handle_command(func: Optional['AnyCallableT'] = None) -> Any:
    """
    Decorator to try a command and handle exceptions gracefull.
    """
    # TODO: Update this logic
    def handle(_func: 'AnyCallable') -> 'AnyCallable':

        @wraps(_func)
        def wrapper_function(*args: Any, **kwargs: Any) -> Any:
            return _func.call(*args, **kwargs)

        return wrapper_function

    if func:
        return handle(func)
    else:
        return handle