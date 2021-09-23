from typing import Callable
from typing import Dict

import typer


ERROR_REGISTRY_TYPE = Dict[BaseException, Callable]

ERROR_REGISTRY: ERROR_REGISTRY_TYPE = {}


def error_handler(*, error):
    """
    Registers a callable function as a way handling a given error class

    @error_handler(error=InvaildInput)
    def handle_invalid_input():
        ...
    """

    def handle(_func):
        if ERROR_REGISTRY.get(error):
            raise ValueError(f"This error - {error} is already registered")

        ERROR_REGISTRY[error] = _func

        return _func

    return handle


@error_handler(error=ValueError)
def print_basic_output_and_exit(error: BaseException):
    typer.echo(f"Handling no image error - {error}")
    raise typer.BadParameter(str(error))
