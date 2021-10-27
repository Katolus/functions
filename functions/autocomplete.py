from typing import Iterator

from functions import user
from functions.docker.helpers import all_functions
from functions.docker.helpers import all_running_functions


def complete_services():
    return ["cloud_function", "cloud_run"]


def autocomplete_function_names(incomplete: str) -> Iterator[str]:
    """Autocompletes a list of matching functions"""
    for function in all_functions():
        if function.name.startswith(incomplete):
            yield function.name


def autocomplete_running_function_names(incomplete: str) -> Iterator[str]:
    """Autocompletes a list of matching functions within running"""
    functions = all_running_functions()
    if not functions:
        user.inform("No running functions")
    for function in functions:
        if function.name.startswith(incomplete):
            yield function.name


def autocomplete_deploy_functions():
    """Specify the functions that are to be deployed"""
    deployable_functions = []
    return deployable_functions
