import sys
from typing import Callable, Dict, NoReturn

import docker

from functions import logs
from functions import styles
from functions import user
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


@error_handler(error=docker.errors.DockerException)
def handle_docker_exception(error: docker.errors.DockerException) -> NoReturn:
    """Handles the base case for all the function errors"""
    logs.exception(error)
    # A temporary solution of handling docker exceptions until we figure out
    # how to handle them in the CLI with different cases.
    user.fail(f"{styles.red('Unexpected docker error occurred')}: {error}.\n")
    user.fail("Please make sure your `docker` is correctly installed.")
    sys.exit(1)
