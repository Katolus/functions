from pathlib import Path
import itertools

import typer

from functions.autocomplete import autocomplete_function_names
from functions.autocomplete import autocomplete_running_function_names
from functions.callbacks import function_name_autocomplete_callback
from functions.callbacks import remove_function_name_callback
from functions.callbacks import running_functions_autocomplete_callback
from functions.commands import gcp
from functions.commands import new
from functions.decorators import handle_error
from functions.docker import all_functions, remove_image
from functions.docker import docker_client
from functions.docker import DockerLabel
from functions.docker import get_config_from_image
from functions.system import get_full_path
from functions.system import load_config
from functions.validation import validate_dir


app = typer.Typer(
    help="Run script to executing, testing and deploying included functions."
)

app.add_typer(gcp.app, name="gcp")
app.add_typer(new.app, name="new")


@app.command()
@handle_error(error_class=ValueError)
def build(
    # TODO: Change to build existing ones first and if not present request a path
    function_path: Path = typer.Argument(
        ...,
        help="Path to the functions you want to build",
    ),
    # TODO: Add an option to show the logs
    show_logs: bool = typer.Option(False, "--force"),
):
    # Get the absolute path
    full_path = get_full_path(function_path)

    # Validate that it is a valid path (throw an error if not)
    validate_dir(full_path)

    # Load configuration
    config = load_config(full_path)

    # TODO: Check if an existing -t exists and ask if overwrite

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
            DockerLabel.CONFIG: str(config_path),
            DockerLabel.ORGANISATION: "Ventress",
            DockerLabel.TAG: function_name,
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
    typer.echo(f"Successfully build a function's image of {function_name}")


@app.command()
def run(
    function_name: str = typer.Argument(
        ...,
        help="Name of the function you want to run",
        autocompletion=autocomplete_function_names,
        callback=function_name_autocomplete_callback,
    ),
):
    """Start a container for a given function"""
    docker_image = docker_client.images.get(function_name)
    config = get_config_from_image(docker_image)

    container = docker_client.containers.run(
        docker_image,
        ports={"8080": config.run_variables.port},
        remove=True,
        name=function_name,
        detach=True,
    )


@app.command()
def stop(
    function_name: str = typer.Argument(
        ...,
        help="Name of the function you want to stop",
        autocompletion=autocomplete_running_function_names,
        callback=running_functions_autocomplete_callback,
    ),
):
    # TODO: Add an option to stop them all
    # TODO: Add a catch for when the name does not match
    container = docker_client.containers.get(function_name)
    container.stop()

    typer.echo(f"Function ({function_name}) has been stopped.")


@app.command()
def list():
    """List existing functions"""
    # TODO: Add a nice format to this list
    # Status
    functions = all_functions()
    if functions:
        for function in functions:
            typer.echo(function)
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
):
    remove_image(function_name)
    typer.echo(f"Function ({function_name}) has been removed")


if __name__ == "__main__":
    app()
