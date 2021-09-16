import functools
from typing import Any, Callable, Optional

import typer


AnyCallableT = Callable[..., Any]


def handle_error(
    func: Optional["AnyCallableT"] = None,
    *,
    error_class: BaseException,
    message_tmp: str = "Something has happened {function_path}"
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

    # Handles a case where function is called as a function as well as a decorator
    # handle_error()(app.command(build))
    # handle_error(app.command(build))

    if func:
        return handle(func)
    else:
        return handle
