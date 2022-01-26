"""Main script for CLI entry point"""
from pathlib import Path
from typing import Optional

import typer

from functions import flows
from functions import logs
from functions import styles
from functions import user
from functions.autocomplete import autocomplete_built_names
from functions.autocomplete import autocomplete_registry_function_names
from functions.autocomplete import autocomplete_running_function_names
from functions.callbacks import check_if_dir_is_a_valid_function_path
from functions.callbacks import check_if_function_is_built
from functions.callbacks import check_if_function_is_running
from functions.callbacks import check_if_name_is_in_registry
from functions.callbacks import print_out_the_version
from functions.config.files import FunctionRegistry
from functions.constants import DEFAULT_LOG_FILEPATH
from functions.constants import LoggingLevel
from functions.core import FunctionsCli
from functions.gcp.cloud_function.errors import GCPCommandError
from functions.logs import set_console_debug_level
from functions.models import Function
from functions.styles import green
from functions.system import follow_file

app = FunctionsCli()


@app.callback()
def main(
    verbose: bool = typer.Option(
        False,
        "--verbose",
        help="Sets the conext of the command to be verbose",
    ),
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        help="Prints out the version of the package",
        callback=print_out_the_version,
        is_eager=True,
    ),
) -> None:
    """
    Manage users in the awesome CLI app.
    """
    # Set logging level
    log_level = LoggingLevel.INFO
    if verbose:
        app.state.verbose = True
        log_level = LoggingLevel.DEBUG
        set_console_debug_level()

    logs.debug(f"Running application in {log_level} logging level.")


@app.command(disable=True)
def error() -> None:
    """A command for testing error messages"""
    user.inform("Message before the error")
    raise GCPCommandError(error_msg="Throwing an error in a test command")


@app.command()
def build(
    function_name: str = typer.Argument(
        ...,
        autocompletion=autocomplete_registry_function_names,
    ),
    disable_logs: bool = typer.Option(True, "--show-logs", help="Show build logs"),
) -> None:
    """Builds an image of a given function"""
    # Get the absolute path
    function = Function(function_name)

    function.build(show_logs=disable_logs)

    user.inform(
        f"{styles.green('Successfully')} build a function's image."
        f" The name of the functions is -> {function_name}"
    )


@app.command()
def run(
    function_name: str = typer.Argument(
        ...,
        help="Name of the function you want to run",
        autocompletion=autocomplete_built_names,
        callback=check_if_function_is_built,
    ),
) -> None:
    """Start a container for a given function"""
    # Guaranteed to exist because of the autocomplete + callback
    function = Function(function_name)

    function.run()

    user.inform(
        f"Function ({function.name}) has {green('started')}."
        f" Visit -> http://localhost:{function.config.run_variables.port}"
    )


@app.command()
def stop(
    function_name: str = typer.Argument(
        ...,
        help="Name of the function you want to stop",
        autocompletion=autocomplete_running_function_names,
        callback=check_if_function_is_running,
    ),
) -> None:
    """Stops a running function"""
    function = Function(function_name)

    function.stop()

    user.inform(f"Function ({function_name}) has been stopped.")


@app.command("list")
def list_functions() -> None:
    """List existing functions"""
    # TODO: Merge docker images and registry functions together
    # functions = all_functions()
    functions = FunctionRegistry.fetch_all_functions()

    # Check if a function is running at the moment
    if functions:
        # Pluralize the word functions based on the number of functions
        plural_function = "functions" if len(functions) > 1 else "function"

        user.inform(f"We found {len(functions)} {plural_function}\n")
        for function in functions:
            user.inform(str(function))
    else:
        user.inform("No functions found")


@app.command()
def remove(
    function_name: str = typer.Argument(
        ...,
        help="Name of the function you want to remove",
        autocompletion=autocomplete_built_names,
        callback=check_if_function_is_built,
    )
) -> None:
    """Removes a local image of a functions"""
    function = Function(function_name)

    user.confirm_abort(f"Are you sure you want to remove the function {function.name}?")

    function.remove()

    user.inform(f"Function {function_name} has been removed.")


@app.command()
def delete(
    function_name: str = typer.Argument(
        ...,
        help="Name of the function you want to remove",
        autocompletion=autocomplete_registry_function_names,
        callback=check_if_name_is_in_registry,
    ),
) -> None:
    """Delete a function from the registry"""
    function = Function(function_name)

    user.confirm_abort(
        " ".join(
            [
                f"Are you sure you want to delete the function {function.name}?.",
                "This means that all attributes associated with this function will be removed.",
            ]
        )
    )

    function.delete_all()

    # Ask a user if they want to remove the underslying resources
    if user.confirm(
        f"Do you want to remove the underlying resources -> {function.config.path}?"
    ):
        function.delete_resources()
        user.inform(f"Resources for {function.name} have been removed.")

    user.inform(f"Function {function.name} has been deleted.")


@app.command()
def add(
    function_dir: Path = typer.Argument(
        ...,
        help="Path to a function's directory you want to add",
        exists=True,
        file_okay=False,
        resolve_path=True,
        callback=check_if_dir_is_a_valid_function_path,
    ),
) -> None:
    """Adds a function to the registry"""
    flows.add_function(str(function_dir))


@app.command(disable=True)
def config() -> None:
    """Renders function's configuration file into the command line"""
    # Print the config if no arguments are provided

    # Remove the config file if --reset flag is passed in
    raise NotImplementedError()


@app.command("logs")
def print_logs() -> None:
    """Prints out function logs"""
    log_path = DEFAULT_LOG_FILEPATH
    # This might be improved if we display limited amount of lines
    with open(log_path, "r") as file:
        for line in follow_file(file):
            print(line, end="")
