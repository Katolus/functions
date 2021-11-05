from typing import Any, Optional

import typer

from functions.callbacks import function_name_callback


# Perhaps there will be a better way to do this, but I'm not sure how.
# Maybe I can use a decorator?
def FunctionNameArgument(
    default: Optional[Any],
    *,
    callback=function_name_callback,
    help="Name of a function in alphabetic constrain [i.e new-function]",
    **kwargs,
) -> Any:
    return typer.models.ArgumentInfo(
        default=default, callback=callback, help=help, **kwargs
    )
