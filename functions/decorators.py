import functools
from typing import Any, Callable, List, Optional, Tuple, Union

import typer
from pydantic import validate_arguments

from functions.errors import FunctionBaseError

AnyCallableT = Callable[..., Any]


@validate_arguments
def handle_error(
    func: Optional["AnyCallableT"] = None,
    *,
    error_class: Tuple[FunctionBaseError, ...],
    message_tmp: str = "Something has happened {function_path}. Error {error}"
):
    """
    Decorator that gracefully handles errors.
    """

    def handle(_func: "AnyCallableT"):
        @functools.wraps(_func)
        def command(*args: Any, **kwargs: Any) -> Any:
            try:
                return _func(*args, **kwargs)
            except error_class as err:
                message = message_tmp.format(error=err, **kwargs)
                raise typer.BadParameter(message)

        return command

    # Handles a case where the decorator is used with arguments and without
    # @handle_error(error_class=FunctionError)
    # @handle_error

    if func:
        return handle(func)
    else:
        return handle


# TODO: Add register_handler and a ERROR_REGISTRY