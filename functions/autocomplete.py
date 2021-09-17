import typer

from functions.docker import all_functions
from functions.docker import all_running_functions


def complete_services():
    return ["cloud_function", "cloud_run"]


def autocomplete_function_names(incomplete: str):
    """Autocompletes a list of matching functions"""
    for function in all_functions():
        if function.startswith(incomplete):
            yield function


def autocomplete_running_function_names(incomplete: str):
    """Autocompletes a list of matching functions within running"""
    functions = all_running_functions()
    if not functions:
        typer.echo("No running functions")
    for function in functions:
        if function.startswith(incomplete):
            yield function


def autocomplete_deploy_functions():
    """Specify the functions that are to be deployed"""
    deployable_functions = []
    # TODO: Find deployable functions
    return deployable_functions
