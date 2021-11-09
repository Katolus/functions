from typing import Callable, Dict, NoReturn

from functions import logs
from functions.errors import FunctionBaseError
from functions.errors import FunctionBuildError
from functions.errors import UsageError
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
    logs.exception(error)
    raise UsageError(error.message)


@error_handler(error=FunctionBuildError)
def handle_function_build_errors(error: FunctionBuildError) -> NoReturn:
    """Handles the base case for all the function errors"""
    # Log the build logs
    logs.debug(error.build_log)  # TODO: Figure out the correct types for this
    logs.exception(error)
    raise UsageError(f"{error.message}. Reason: {error.reason}")
