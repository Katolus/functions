"""Stores methods for validating GCP commands using typer's callback method"""
import typer

from functions.config.errors import FunctionNotInRegistryError
from functions.config.files import FunctionRegistry
from functions.gcp.cloud_function import cli as cf_cli


def gcp_logs_callback(
    ctx: typer.Context, param: typer.CallbackParam, function_name: str
) -> str:
    """Validates the GCP logs command"""
    # Check if the function name is in the function registry
    if FunctionRegistry.check_if_function_in_registry(function_name):
        # Check if the function is a GCP function
        cloud_functions = cf_cli.fetch_function_names()
    else:
        raise FunctionNotInRegistryError(function=function_name)

    return function_name
