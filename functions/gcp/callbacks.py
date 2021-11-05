"""Stores methods for validating GCP commands using typer's callback method"""
import typer

from functions.config.errors import FunctionNotInRegistryError
from functions.config.files import FunctionRegistry
from functions.gcp.cloud_function import cli as cf_cli


def gcp_deploy_callback(
    ctx: typer.Context, param: typer.CallbackParam, function_name: str
) -> str:
    """Validates the GCP deploy command"""
    # Check if the function name is in the function registry
    if FunctionRegistry.check_if_function_name_in_registry(function_name):
        return function_name
    else:
        raise FunctionNotInRegistryError(function=function_name)


def gcp_logs_callback(
    ctx: typer.Context, param: typer.CallbackParam, function_name: str
) -> str:
    """Validates the GCP logs command"""
    # Check if the function name is in the function registry
    if FunctionRegistry.check_if_function_name_in_registry(function_name):
        # Check if the function is a GCP function
        _ = cf_cli.fetch_function_names()
    else:
        raise FunctionNotInRegistryError(function=function_name)

    return function_name
