from typing import Optional

import typer

from functions import __project_name__
from functions import __version__
from functions import styles
from functions.autocomplete import autocomplete_function_names
from functions.autocomplete import autocomplete_running_function_names
from functions.config.models import FunctionConfig
from functions.decorators import handle_error
from functions.decorators import resilient_parsing
from functions.docker.helpers import all_functions
from functions.errors import FunctionNameTaken
from functions.user import confirm_abort
from functions.validators import validate_name


@handle_error
def version_callback(value: bool) -> None:
    """Prints out the version of the package and exists"""
    if value:
        typer.echo(
            f"You are using {styles.bold(__version__)} version of the "
            f"{styles.bold(__project_name__)} package"
        )
        raise typer.Exit()


@handle_error
def build_function_callack(
    ctx: typer.Context, param: typer.CallbackParam, function_path: str
):
    """
    Check if a function name is already an existing function image. Throw an error if so
    """
    config = FunctionConfig.load(function_path)
    built_function_names = [function.name for function in all_functions()]

    if config.run_variables.name in built_function_names:
        raise FunctionNameTaken(name=config.run_variables.name)

    return function_path


@resilient_parsing
def function_name_callback(
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
def function_name_autocomplete_callback(
    ctx: typer.Context, param: typer.CallbackParam, value: str
) -> Optional[str]:

    build_functions = list(autocomplete_function_names(""))
    if build_functions and value not in build_functions:
        raise typer.BadParameter(
            f"You can only run build functions {build_functions}."
            " Use autocomplete the pass a valid name."
        )

    return value


@resilient_parsing
def running_functions_autocomplete_callback(
    ctx: typer.Context, param: typer.CallbackParam, value: str
) -> Optional[str]:
    if (
        running_functions := list(autocomplete_running_function_names(""))
    ) and value not in running_functions:
        raise typer.BadParameter(
            f"You can only stop already running functions {running_functions}."
            " Use autocomplete the pass a valid name."
        )

    return value


@resilient_parsing
def remove_function_name_callback(
    ctx: typer.Context, param: typer.CallbackParam, value: str
) -> Optional[str]:
    if (
        running_functions := list(autocomplete_running_function_names(""))
    ) and value not in running_functions:
        raise typer.BadParameter(
            f"You can only remove existing functions {running_functions}."
            " Use autocomplete the pass a valid name."
        )

    return value


@resilient_parsing
def generate_new_function_callback(
    ctx: typer.Context, param: typer.CallbackParam, value: str
) -> Optional[str]:
    """Callback for generating a new function"""
    if not value or value == ".":
        confirm_abort("Are you sure you want to use the current directory?")
        value = "."

    return value


def add_callback(ctx: typer.Context, param: typer.CallbackParam, value: str) -> str:
    """Validates a call to the `add` command"""
    return value
