"""Stores methods for validating GCP commands using typer's callback method"""
import typer

from functions.config.errors import FunctionNotInRegistryError
from functions.config.files import FunctionRegistry


def check_if_function_name_in_registry(
    ctx: typer.Context, param: typer.CallbackParam, function_name: str
) -> str:
    """Validates the GCP deploy command"""
    # Check if the function name is in the function registry
    if FunctionRegistry.check_if_function_name_in_registry(function_name):
        return function_name
    else:
        raise FunctionNotInRegistryError(function=function_name)
