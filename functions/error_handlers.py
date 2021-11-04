from typing import Callable, Dict, NoReturn

import typer

from functions import logs
from functions import user
from functions.errors import FunctionBaseError
from functions.errors import FunctionNameTaken
from functions.types import AnyCallable
from functions.types import ExceptionClass

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


@error_handler(error=FunctionBaseError)
def handle_function_all_errors(error: FunctionBaseError) -> NoReturn:
    """Handles the base case for all the function errors"""
    logs.error(error)
    user.fail(error.message)
    raise typer.BadParameter(error.message)


@error_handler(error=ValueError)
def print_basic_output_and_exit(error: ExceptionClass) -> NoReturn:
    user.inform(f"Handling no image error - {error}")
    raise typer.BadParameter(str(error))


@error_handler(error=FunctionNameTaken)
def handle_function_name_with_suggestion(error: ExceptionClass) -> NoReturn:
    error_msg = str(error)
    user.inform(f"Error: {error_msg}")
    user.inform("Unable to continue. See the errors")
    # Verbose - Consider renaming the function or removing the old one
    raise typer.Exit()
