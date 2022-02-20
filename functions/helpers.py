from functions.config.files import FunctionRegistry
from functions.constants import LocalStatus


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
