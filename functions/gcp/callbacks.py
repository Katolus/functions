"""Stores methods for validating GCP commands using typer's callback method"""
import typer

from functions.config.files import FunctionRegistry
from functions.helpers import is_function_in_registry
from functions.helpers import is_function_source_valid


def check_if_function_name_in_registry(
    ctx: typer.Context, param: typer.CallbackParam, function_name: str
) -> str:
    """Validates the GCP deploy command"""
    # Check if the function name is in the function registry
    if FunctionRegistry.check_if_function_name_in_registry(function_name):
        return function_name
    else:
        raise typer.BadParameter(
            f"Function '{function_name}' not found in registry. "
            "Please check the function name and try again."
        )


def check_if_function_can_be_deployed(
    ctx: typer.Context, param: typer.CallbackParam, f_name: str
) -> str:
    """Checks if a function can be deployed to GCP"""
    # Check if the function name is in the function registry
    if not is_function_in_registry(f_name):
        raise typer.BadParameter(
            f"Function '{f_name}' not found in registry. "
            "Please check the function name and try again."
        )

    if not is_function_source_valid(f_name):
        raise typer.BadParameter(
            f"Function '{f_name}' source is not valid. Please fix it and try again."
        )

    return f_name
