import json
import itertools
from pathlib import Path
from typing import Optional

import typer

from functions.autocomplete import autocomplete_function_names
from functions.autocomplete import autocomplete_running_function_names
from functions.callbacks import function_name_autocomplete_callback, version_callback
from functions.callbacks import remove_function_name_callback
from functions.callbacks import running_functions_autocomplete_callback
from functions.commands import gcp
from functions.commands import new
from functions.constants import DockerLabel
from functions.core import Functions
from functions.docker.client import docker_client
from functions.docker.helpers import all_functions
from functions.docker.helpers import get_config_from_image
from functions.docker.tools import remove_image
from functions.styles import blue, red
from functions.system import construct_config_path, get_full_path
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
    # TODO: Change to build existing ones first and if not present request a path
    function_path: Path = typer.Argument(
        ...,
        help="Path to the functions you want to build",
    ),
    # TODO: Add an option to show the logs
    show_logs: bool = typer.Option(False, "--force"),
) -> None:
    """Builds an image of a given function"""
    # Get the absolute path
    full_path = get_full_path(function_path)

    # Load configuration
    config = load_config(full_path)

    # TODO: Check if an existing function image already exist and ask if to overwrite

    # Formulate a function tag
    function_name = config.run_variables.name
    build_kwargs = {
        "path": str(full_path),
        "tag": function_name,
        "buildargs": {
            "TARGET": config.run_variables.entry_point,
            "SOURCE": config.run_variables.source,
            "SIGNATURE_TYPE": config.run_variables.signature_type,
        },
        # TODO: Store a configuration path as a label
        "labels": {
            DockerLabel.FUNCTION_NAME: function_name,
            DockerLabel.FUNCTION_PATH: str(full_path),
            DockerLabel.CONFIG_PATH: str(construct_config_path(full_path)),
            DockerLabel.CONFIG: json.dumps(config.json()),
            DockerLabel.ORGANISATION: "Ventress",
        },
    }

    # TODO: Check if the port is in use

    # TODO: Add BuildError from docker
    # TODO: Move to docker.py
    if show_logs:
        from docker.utils.json_stream import json_stream

        resp = docker_client.api.build(**build_kwargs)
        result_stream, internal_stream = itertools.tee(json_stream(resp))
        for result in result_stream:
            print(result)
    else:
        image, logs = docker_client.images.build(**build_kwargs)

    # TODO: Add color
    typer.echo(
        f"Successfully build a function's image. The name of the functions is -> {function_name}"
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
    docker_image = docker_client.images.get(function_name)
    config = get_config_from_image(docker_image)

    # TODO: Move to docker tools
    container = docker_client.containers.run(
        docker_image,
        ports={"8080": config.run_variables.port},
        remove=True,
        name=function_name,
        detach=True,
    )

    # TODO: Add information about how is it available

    typer.echo(f"Function ({container.name}) has started.")


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
    # TODO: Add an option to stop them all
    # TODO: Add a catch for when the name does not match
    container = docker_client.containers.get(function_name)
    container.stop()

    typer.echo(f"Function ({function_name}) has been stopped.")


@app.command()
def list() -> None:
    """List existing functions"""
    functions = all_functions()
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


# TODO: Add config command if useful
