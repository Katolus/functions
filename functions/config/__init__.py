"""Top level module for all configuration related"""
from functions import logs
from functions.constants import FunctionStatus

from .files import FunctionRegistry
from .models import FunctionRecord


def store_function_info_to_registry(
    function: FunctionRecord, *, status: FunctionStatus
) -> None:
    """Add a function to the registry"""
    function.status = status
    if FunctionRegistry.check_if_function_name_in_registry(function.name):
        logs.debug(f"FunctionRegistry: Updating function {function.name} ({status})")
        FunctionRegistry.update_function(function)
    else:
        logs.debug(f"FunctionRegistry: Adding function {function.name} ({status})")
        FunctionRegistry.add_function(function)


def remove_function_from_registry(function_name: str) -> None:
    """Remove a function from the registry"""
    FunctionRegistry.remove_function(function_name)
