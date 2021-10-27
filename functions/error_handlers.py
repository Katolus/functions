from typing import Callable
from typing import Dict
from typing import NoReturn

import typer

from functions.types import AnyCallable, ExceptionClass
from functions.errors import ConfigValidationError, FunctionNameTaken


ERROR_REGISTRY_TYPE = Dict[ExceptionClass, Callable]

ERROR_REGISTRY: ERROR_REGISTRY_TYPE = {}


def error_handler(*, error: ExceptionClass) -> AnyCallable:
    """
    Registers a callable function as a way handling a given error class

    @error_handler(error=InvaildInput)
    def handle_invalid_input():
        ...
    """

    def handle(_func) -> AnyCallable:
        if ERROR_REGISTRY.get(error):
            raise ValueError(f"This error - {error} is already registered")

        ERROR_REGISTRY[error] = _func

        return _func

    return handle


@error_handler(error=ValueError)
def print_basic_output_and_exit(error: ExceptionClass) -> NoReturn:
    typer.echo(f"Handling no image error - {error}")
    raise typer.BadParameter(str(error))


@error_handler(error=ConfigValidationError)
def check_config_in_path(error: ExceptionClass) -> NoReturn:
    # Print a path where this is saved
    raise typer.BadParameter(str(error))


@error_handler(error=FunctionNameTaken)
def handle_function_name_with_suggestion(error: ExceptionClass) -> NoReturn:
    error_msg = str(error)
    typer.echo(f"Error: {error_msg}", err=True)
    typer.echo(f"Unable to continue. See the errors", err=True)
    # Verbose - Consider renaming the function or removing the old one
    raise typer.Exit()
    