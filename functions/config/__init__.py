"""Top level module for all configuration related"""
from functions.constants import FunctionStatus
from functions.logs import debug

from .files import FunctionRegistry
from .models import FunctionConfig
from .models import FunctionRecord


def store_function_info_to_registry(
    function_name: str, function_config: FunctionConfig, status: FunctionStatus
) -> None:
    """Add a function to the registry"""
    if FunctionRegistry.check_if_function_in_registry(function_name):
        debug(f"FunctionRegistry: Updating function {function_name}")
        FunctionRegistry.update_function(
            FunctionRecord(name=function_name, config=function_config, status=status)
        )
    else:
        FunctionRegistry.add_function(
            FunctionRecord(name=function_name, config=function_config, status=status)
        )


def remove_function_from_registry(function_name: str) -> None:
    """Remove a function from the registry"""
    FunctionRegistry.remove_function(function_name)
