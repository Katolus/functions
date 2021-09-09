import typer

from functions.autocomplete import autocomplete_function_names, complete_function_dir
from functions.config import load_config
from functions.docker import (
    DockerLabel,
    docker_client,
    get_config_from_image,
)  # TODO: Find a better way of doing this (global variables)
from functions.system import construct_config_path, get_full_path
from functions.validation import validate_dir


app = typer.Typer(help="Run a function using docker")


@app.command()
def build(
    function_path: str = typer.Argument(
        ...,
        help="Path to the functions you want to build",
    ),
    config_name: str = typer.Option("config.json", help="Name of a config file"),
):
    # Get the absolute path
    full_path = get_full_path(function_path)

    # Validate that it is a valid path (throw an error if not)
    validate_dir(full_path)

    # Load configuration
    config_path = construct_config_path(full_path, config_name)
    config = load_config(config_path)

    # TODO: Check if an existing -t exists and ask if overwrite

    # Formulate a function tag
    function_name = config.run_variables.name

    image, logs = docker_client.images.build(
        path=str(full_path),
        tag=function_name,
        # buildargs={"CONFIG_PATH": config_path, "FUNC_TAG": function_name},
        labels={
            DockerLabel.CONFIG: str(config_path),
            DockerLabel.ORGANISATION: "Ventress",
            DockerLabel.TAG: function_name,
        },
    )

    # TODO: Add color
    typer.echo(f"Successfully build a function's image of {function_name}")


@app.command()
def start(
    function_name: str = typer.Argument(
        ...,
        help="Name of the function you are running.",
        autocompletion=autocomplete_function_names,
    ),
):
    """Start a container for a given function"""
    docker_image = docker_client.images.get(function_name)
    config = get_config_from_image(docker_image)

    container = docker_client.containers.run(
        docker_image,
        ports={config.run_variables.port: "8080"},
        remove=True,
        name=function_name,
        detach=True,
    )


@app.command()
def stop(
    function_name: str = typer.Argument(
        ...,
        help="Name of the functions to stop",
    ),
):
    # TODO: Add a catch for when the name does not match
    container = docker_client.containers.get(function_name)
    container.stop()


@app.command()
def status(
    function_name: str = typer.Option(
        None,
        help="Give status of a function",
        autocompletion=complete_function_dir,
    ),
):

    ...


@app.command()
def list(
    function_name: str = typer.Argument(
        "",
        help="List existing functions",
    ),
):
    ...
