from typing import Iterator

from functions.config.files import FunctionRegistry
from functions.constants import LocalStatus


def autocomplete_registry_function_names(incomplete: str) -> Iterator[str]:
    """Autocompletes a list of matching functions within registry"""
    for function_name in FunctionRegistry.fetch_function_names():
        if function_name.startswith(incomplete):
            yield function_name


def autocomplete_built_names(incomplete: str) -> Iterator[str]:
    """Autocompletes a list of matching functions"""
    for function_name in FunctionRegistry.fetch_built_function_names():
        if function_name.startswith(incomplete):
            yield function_name


def autocomplete_running_function_names(incomplete: str) -> Iterator[str]:
    """Autocompletes a list of matching functions within running"""
    for function_name in FunctionRegistry.fetch_local_function_names(
        LocalStatus.RUNNING
    ):
        if function_name.startswith(incomplete):
            yield function_name


def autocomplete_gcp_deployed_functions(incomplete: str) -> Iterator[str]:
    """Specify the functions that are to be deployed"""
    for function_name in FunctionRegistry.fetch_gcp_function_names():
        if function_name.startswith(incomplete):
            yield function_name
