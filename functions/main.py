from pathlib import Path
from typing import Optional

import typer

from functions import styles
from functions.autocomplete import autocomplete_function_names
from functions.autocomplete import autocomplete_running_function_names
from functions.callbacks import (
    build_function_callack,
    function_name_autocomplete_callback,
    version_callback,
)
from functions.callbacks import remove_function_name_callback
from functions.callbacks import running_functions_autocomplete_callback
from functions.commands import gcp
from functions.commands import new
from functions.core import Functions
from functions.docker.helpers import all_functions, get_config_from_image
from functions.docker.tools import (
    build_image,
    get_image,
    remove_image,
    run_container,
    stop_container,
)
from functions.styles import blue, red
from functions.system import get_full_path
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
    if verbose:
        # typer.echo("Will write verbose output") ## log
        app.state.verbose = True


@app.command()
def test() -> None:
    """Test command not to be dispayed"""
    raise ValueError
    typer.echo("End of test command")


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
    full_path = get_full_path(function_path)

    # Load configuration
    config = load_config(full_path)

    image = build_image(config, show_logs)
    # TODO: Update the log that prints out the information to the console

    typer.echo(
        f"{styles.green('Successfully')} build a function's image. The name of the functions is -> {config.run_variables.name}"
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

    typer.echo(
        f"Function ({container.name}) has started. Visit -> http://localhost:{config.run_variables.port}"
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
    typer.echo(f"Function ({function_name}) has been stopped.")


@app.command()
def list() -> None:
    """List existing functions"""
    functions = all_functions()
    # Check if a function is running at the moment
    if app.state.verbose:
        typer.echo(f"Will write verbose lists")
    if functions:
        typer.echo(f"There are {len(functions)} build and available.\n")
        for function in functions:
            typer.echo(
                f"Function - {red(function.name)} | Status - {blue(function.status)}"
            )
    else:
        typer.echo("No functions found")


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
    typer.echo(f"Function ({function_name}) has been removed")


@app.command()
def config() -> None:
    """Renders function's configuration file into the command line"""
    ...

@app.command()
def rebuild() -> None:
    """Rebuild a function if it is possible"""
    ...


