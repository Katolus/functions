from functions.autocomplete import (
    autocomplete_function_names,
    autocomplete_running_function_names,
)
from typing import Optional

import typer

from functions.validators import str_is_alpha_validator
from functions.types import LocalFunctionPath
from functions.input import confirm_abort


def function_name_callback(
    ctx: typer.Context, param: typer.CallbackParam, value: str
) -> Optional[str]:
    if ctx.resilient_parsing:
        return None

    try:
        # TODO: Update this to correctly filter invalid names (regex?)
        str_is_alpha_validator(value)
    except ValueError:
        raise typer.BadParameter(
            "Only alphabetic characters are allowed as function names"
        )
    return value


def function_name_autocomplete_callback(
    ctx: typer.Context, param: typer.CallbackParam, value: str
) -> Optional[str]:
    if ctx.resilient_parsing:
        return None

    build_functions = list(autocomplete_function_names(""))
    # TODO: Check if the container is running and abort if it already is running
    if build_functions and value not in build_functions:
        raise typer.BadParameter(
            f"You can only run build functions {build_functions}. Use autocomplete the pass a valid name."
        )

    return value


def running_functions_autocomplete_callback(
    ctx: typer.Context, param: typer.CallbackParam, value: str
) -> Optional[str]:
    if ctx.resilient_parsing:
        return None

    if (
        running_functions := list(autocomplete_running_function_names(""))
    ) and value not in running_functions:
        raise typer.BadParameter(
            f"You can only stop already running functions {running_functions}. Use autocomplete the pass a valid name."
        )

    return value




# TODO: Add a decorator for the resilient_parsing
def remove_function_name_callback(
    ctx: typer.Context, param: typer.CallbackParam, value: str
) -> Optional[str]:
    if ctx.resilient_parsing:
        return None

    if (
        running_functions := list(autocomplete_running_function_names(""))
    ) and value not in running_functions:
        raise typer.BadParameter(
            f"You can only remove existing functions {running_functions}. Use autocomplete the pass a valid name."
        )

    return value


def function_dir_callback(
    ctx: typer.Context, param: typer.CallbackParam, value: str
) -> Optional[str]:
    if ctx.resilient_parsing:
        return None

    if not value or value == ".":
        confirm_abort("Are you sure you want to use the current directory?")
        value = "."

    # Find a better way of doing this
    local_dir: LocalFunctionPath = value

    return str(local_dir)
