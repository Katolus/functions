"""Top level module for all configuration related"""
from functions.logs import debug

from .files import FunctionRegistry
from .models import FunctionConfig
from .models import FunctionRecord


def add_function_to_registry(
    function_name: str, function_config: FunctionConfig
) -> None:
    """Add a function to the registry"""
    debug(f"Adding function {function_name} to registry")
    FunctionRegistry.add_function(
        FunctionRecord(name=function_name, config=function_config)
    )


def remove_function_from_registry(function_name: str) -> None:
    """Remove a function from the registry"""
    debug(f"Removing function {function_name} from registry")
    FunctionRegistry.remove_function(function_name)
