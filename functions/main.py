from pathlib import Path
from typing import Optional

import typer

from functions import logs
from functions import styles
from functions import user
from functions.autocomplete import autocomplete_function_names
from functions.autocomplete import autocomplete_running_function_names
from functions.callbacks import build_function_callack
from functions.callbacks import function_name_autocomplete_callback
from functions.callbacks import remove_function_name_callback
from functions.callbacks import running_functions_autocomplete_callback
from functions.callbacks import version_callback
from functions.commands import gcp
from functions.commands import new
from functions.config import add_function_to_registry
from functions.config import remove_function_from_registry
from functions.constants import LoggingLevel
from functions.core import Functions
from functions.docker.helpers import all_functions
from functions.docker.helpers import get_config_from_image
from functions.docker.tools import build_image
from functions.docker.tools import get_image
from functions.docker.tools import remove_image
from functions.docker.tools import run_container
from functions.docker.tools import stop_container
from functions.logs import set_console_handler_level
from functions.styles import blue
from functions.styles import green
from functions.styles import red
from functions.system import construct_abs_path
from functions.system import load_config

app = Functions(subcommands=[(new.app, "new"), (gcp.app, "gcp")])


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
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """
    Manage users in the awesome CLI app.
    """
    log_level = LoggingLevel.INFO
    if verbose:
        app.state.verbose = True
        log_level = LoggingLevel.DEBUG

    set_console_handler_level(log_level)
    logs.debug(f"Running application in {log_level} logging level.")


@app.command()
def test() -> None:
    """Test command not to be dispayed"""
    user.inform("Running a test command")
    raise ValueError("Throwing an error in a test command")


@app.command()
def build(
    function_path: Path = typer.Argument(
        ...,
        help="Path to the functions you want to build",
        callback=build_function_callack,
    ),
    show_logs: bool = typer.Option(False, "--show-logs", help="Show build logs"),
) -> None:
    """Builds an image of a given function"""
    # Get the absolute path
    full_path = construct_abs_path(function_path)

    # Load configuration
    config = load_config(full_path)

    _ = build_image(config, show_logs)

    function_name = config.run_variables.name
    # store the function details in the config
    add_function_to_registry(function_name, config)

    user.inform(
        f"{styles.green('Successfully')} build a function's image."
        " The name of the functions is -> {function_name}"
    )


@app.command()
def run(
    function_name: str = typer.Argument(
        ...,
        help="Name of the function you want to run",
        autocompletion=autocomplete_function_names,
        callback=function_name_autocomplete_callback,
    ),
) -> None:
    """Start a container for a given function"""

    function_image = get_image(function_name)
    config = get_config_from_image(function_image)
    container = run_container(function_image, config)

    user.inform(
        f"Function ({container.name}) has {green('started')}."
        " Visit -> http://localhost:{config.run_variables.port}"
    )


@app.command()
def stop(
    function_name: str = typer.Argument(
        ...,
        help="Name of the function you want to stop",
        autocompletion=autocomplete_running_function_names,
        callback=running_functions_autocomplete_callback,
    ),
) -> None:
    """Stops a running function"""
    stop_container(function_name)
    user.inform(f"Function ({function_name}) has been stopped.")


@app.command("list")
def list_functions() -> None:
    """List existing functions"""
    functions = all_functions()
    # Check if a function is running at the moment
    if functions:
        logs.debug(f"Found {len(functions)} functions.")
        user.inform(f"There are {len(functions)} build and available.\n")
        for function in functions:
            user.inform(
                f"Function - {red(function.name)} | Status - {blue(function.status)}"
            )
    else:
        user.inform("No functions found")


@app.command()
def remove(
    function_name: str = typer.Argument(
        ...,
        help="Name of the function you want to remove",
        autocompletion=autocomplete_function_names,
        callback=remove_function_name_callback,
    )
) -> None:
    """Removes an image of a functions from the local registry"""
    remove_image(function_name)
    remove_function_from_registry(function_name)
    user.inform(f"Function ({function_name}) has been removed")


@app.command()
def config() -> None:
    """Renders function's configuration file into the command line"""
    raise NotImplementedError()


@app.command()
def rebuild(
    function_name: str = typer.Argument(
        ...,
        help="Name of the function you want to rebuild",
        autocompletion=autocomplete_function_names,
    ),
    show_logs: bool = typer.Option(False, "--show-logs", help="Show build logs"),
) -> None:
    """Rebuild a function if it is possible"""
    functions = all_functions()

    for function in functions:
        if function.name == function_name:
            build_image(function.config, show_logs)
            raise typer.Exit()

    user.inform("No functions found")
