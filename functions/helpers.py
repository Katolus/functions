from functions.config.files import FunctionRegistry
from functions.constants import LocalStatus
from functions.models import Function


def is_function_in_registry(function_name: str) -> bool:
    """Checks if a function is in the registry"""
    if function_name in FunctionRegistry.fetch_function_names():
        return True
    return False


def is_function_built(function_name: str) -> bool:
    """Checks if a function is built"""
    built_functions = FunctionRegistry.fetch_built_function_names()
    if built_functions and function_name in built_functions:
        return True
    return False


def is_function_running(function_name: str) -> bool:
    """Checks if a function is running"""
    running_functions = FunctionRegistry.fetch_local_function_names(
        status=LocalStatus.RUNNING
    )
    if running_functions and function_name in running_functions:
        return True
    return False


def is_function_source_valid(function_name: str) -> bool:
    """Checks if a function source is valid"""
    function = Function(function_name)
    return function.config.is_source_valid()
