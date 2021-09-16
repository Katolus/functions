from typing import Any, Optional

import typer

from functions.callbacks import function_name_callback


# Not the best cause we are loosing types
def FunctionNameArgument(
    default: Optional[Any],
    *,
    callback=function_name_callback,
    help="Name of a function in alphabetic constrain [i.e new-function]",
    **kwargs
) -> Any:
    return typer.models.ArgumentInfo(
        default=default, callback=callback, help=help, **kwargs
    )
