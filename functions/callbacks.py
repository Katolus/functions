from typing import Optional

import typer

from functions import __package_name__
from functions import __version__
from functions import styles
from functions import user
from functions.config.files import FunctionRegistry
from functions.constants import LocalStatus
from functions.decorators import handle_error
from functions.decorators import resilient_parsing
from functions.user import confirm_abort
from functions.validators import validate_name


@handle_error
def print_out_the_version(value: bool) -> None:
    """Prints out the version of the package and exists"""
    if value:
        user.inform(
            f"You are using {styles.bold(__version__)} version of the "
            f"{styles.bold(__package_name__)} package"
        )
        raise typer.Exit()


@resilient_parsing
def check_if_name_is_a_valid_string(
    ctx: typer.Context, param: typer.CallbackParam, value: str
) -> Optional[str]:
    # TODO: Add a check to see if the function name is already taken
    try:
        validate_name(value)
    except ValueError:
        # TODO: Update this to throw a custom error
        raise typer.BadParameter(
            "Only alphabetic characters with '-' and '_' characters are allowed"
            " as function names"
        )
    return value


@resilient_parsing
def check_if_name_is_in_registry(
    ctx: typer.Context, param: typer.CallbackParam, value: str
) -> Optional[str]:
    """Callback that validates if a function name is in the registry"""
    if value not in FunctionRegistry.fetch_function_names():
        raise typer.BadParameter(
            f"{value} is not a valid function name. "
            "Please use one of the following: "
            f"{', '.join(FunctionRegistry.fetch_function_names())}"
        )
    return value


@resilient_parsing
def check_if_function_is_built(
    ctx: typer.Context, param: typer.CallbackParam, value: str
) -> Optional[str]:

    build_functions = FunctionRegistry.fetch_built_function_names()
    if build_functions and value not in build_functions:
        raise typer.BadParameter(
            f"You can only run build functions {build_functions}."
            " Use autocomplete the pass a valid name."
        )

    return value


@resilient_parsing
def check_if_function_is_running(
    ctx: typer.Context, param: typer.CallbackParam, value: str
) -> Optional[str]:
    running_functions = FunctionRegistry.fetch_local_function_names(
        status=LocalStatus.RUNNING
    )
    if running_functions and value not in running_functions:
        raise typer.BadParameter(
            f"You can only stop already running functions {running_functions}."
            " Use autocomplete the pass a valid name."
        )

    return value


@resilient_parsing
def confirm_current_directory_as_target(
    ctx: typer.Context, param: typer.CallbackParam, value: str
) -> Optional[str]:
    """Callback for generating a new function"""
    if not value or value == ".":
        confirm_abort("Are you sure you want to use the current directory?")
        value = "."

    return value


def check_if_dir_is_a_valid_function_path(
    ctx: typer.Context, param: typer.CallbackParam, value: str
) -> str:
    """Callback that validates a target directory"""
    # TODO: Add a check to see if the function name is already taken
    # TODO: Check if the path is a valid path
    return value
