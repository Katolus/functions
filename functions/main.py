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
from functions.callbacks import check_if_function_can_be_built
from functions.callbacks import check_if_function_can_be_removed
from functions.callbacks import check_if_function_can_be_run
from functions.callbacks import check_if_function_can_be_stopped
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
        help="Enable verbose logging",
    ),
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        help="Print the version and exit",
        callback=print_out_the_version,
        is_eager=True,
    ),
) -> None:
    """
    CLI entry point for functions.

    This code will run when you run `functions` from the command line.
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
def add(
    function_dir: Path = typer.Argument(
        ...,
        help="The directory of the function to add",
        exists=True,
        file_okay=False,
        resolve_path=True,
        callback=check_if_dir_is_a_valid_function_path,
    ),
) -> None:
    """
    Add a function to the function registry.
    """
    flows.add_function(str(function_dir))


@app.command()
def build(
    function_name: str = typer.Argument(
        ...,
        help="The name of the function to build",
        autocompletion=autocomplete_registry_function_names,
        callback=check_if_function_can_be_built,
    ),
    show_logs: bool = typer.Option(False, "--show-logs", help="Show build output"),
) -> None:
    """
    Build a function.
    """
    # Get the absolute path
    function = Function(function_name)

    function.build(show_logs=show_logs)

    user.inform(
        f"{styles.green('Successfully')} build a function's image."
        f" The name of the functions is -> {function_name}"
    )


@app.command("list")
def list_functions() -> None:
    """
    List all functions in the registry.
    """
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
def run(
    function_name: str = typer.Argument(
        ...,
        help="The name of the function to run",
        autocompletion=autocomplete_built_names,
        callback=check_if_function_can_be_run,
    ),
) -> None:
    """
    Run a function locally using the built image.
    """
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
        help="The name of the function to stop",
        autocompletion=autocomplete_running_function_names,
        callback=check_if_function_can_be_stopped,
    ),
) -> None:
    """
    Stop a function running locally.
    """
    function = Function(function_name)

    function.stop()

    user.inform(f"Function ({function_name}) has been stopped.")


@app.command()
def remove(
    function_name: str = typer.Argument(
        ...,
        help="The name of the function to remove",
        autocompletion=autocomplete_built_names,
        callback=check_if_function_can_be_removed,
    )
) -> None:
    """
    Remove a function from the registry.
    """
    function = Function(function_name)

    user.confirm_abort(f"Are you sure you want to remove the function {function.name}?")

    function.remove()

    user.inform(f"Function {function_name} has been removed.")


@app.command()
def delete(
    function_name: str = typer.Argument(
        ...,
        help="The name of the function to delete",
        autocompletion=autocomplete_registry_function_names,
        callback=check_if_name_is_in_registry,
    ),
) -> None:
    """
    Delete a function with all its data from the registry.
    """
    function = Function(function_name)

    user.confirm_abort(
        " ".join(
            [
                f"Are you sure you want to delete the function {function.name}?.",
                "This means that all information associated with this function will be removed.",
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


@app.command(disable=True)
def config() -> None:
    """Renders function's configuration file into the command line"""
    # Print the config if no arguments are provided

    # Remove the config file if --reset flag is passed in
    raise NotImplementedError()


@app.command("logs")
def print_logs() -> None:
    """
    Print the logs of functions CLI.
    """
    log_path = DEFAULT_LOG_FILEPATH
    # This might be improved if we display limited amount of lines
    with open(log_path, "r") as file:
        for line in follow_file(file):
            print(line, end="")
