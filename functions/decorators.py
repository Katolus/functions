import functools
from typing import Any, Callable, Optional, Tuple

import typer
from pydantic import validate_arguments

from functions.errors import FunctionBaseError
from functions.error_handlers import ERROR_REGISTRY

AnyCallableT = Callable[..., Any]


@validate_arguments
def handle_error(
    func: Optional["AnyCallableT"] = None,
    *,
    error_class: Optional[Tuple[FunctionBaseError, ...]] = None,
    message_tmp: str = "Something has happened. Error {error}",
):
    """
    Decorator that gracefully handles errors.
    """

    def handle(_func: AnyCallableT):
        @functools.wraps(_func)
        def command(*args: Any, **kwargs: Any) -> Any:
            try:
                return _func(*args, **kwargs)
            except Exception as err:
                
                # Check initial params for handlers
                if error_class and isinstance(err, error_class):
                    message = message_tmp.format(error=err, **kwargs)
                    raise typer.BadParameter(message)

                # Check registry for handlers
                if handler := ERROR_REGISTRY.get(err.__class__):
                    handler(err)
                else:
                    # If nothing matches reraise exception
                    raise err

        return command

    # Handles a case where the decorator is used with arguments and without
    # @handle_error(error_class=FunctionError)
    # @handle_error

    if func:
        return handle(func)
    else:
        return handle


CallbackCallable = Callable[[typer.Context, typer.CallbackParam, str], Optional[str]]


def resilient_parsing(func) -> CallbackCallable:
    """Wraps a callback functions to return for resilient parsing [Typer]"""

    @functools.wraps(func)
    def wrapper(
        ctx: typer.Context, param: typer.CallbackParam, value: str
    ) -> Optional[str]:
        if ctx.resilient_parsing:
            return None

        return func(ctx, param, value)

    return wrapper
