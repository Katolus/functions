import os
import subprocess
from pathlib import Path
from typing import Iterable, List

import typer
from pydantic import ValidationError

app = typer.Typer(help="Run a function using docker")

from functions.autocomplete import complete_function_dir
from functions.config import load_config
from functions.processes import run_cmd
from functions.validation import validate_dir
from functions.hints import DockerImage


def get_full_path(function_path: str) -> Path:
    """Returns a full path of a function"""
    return Path(os.path.abspath(os.path.join(os.getcwd(), function_path)))


def get_functions():
    output = run_cmd(
        [
            "docker",
            "images",
            "--format",
            "{{.ID}}:{{.Repository}}:{{.Tag}}:{{.CreatedSince}}:{{.Size}}",
            "--filter",
            "label=package.functions.marker=Ventress",
        ],
        capture_output=True,
    )
    cmd_output = output.stdout.decode("utf-8").strip()
    if cmd_output:
        functions: List[str] = cmd_output.split("\n")
        images: List[DockerImage] = []

        for function in functions:
            # Remove multiple whitespaces and split on delimeter
            # Format: 92ec30fd5d23:<none>:<none>:21 hours ago:135MB
            function_vars = function.strip().split(":")
            images.append(DockerImage(*function_vars))

        return images
    else:
        raise ValueError("No function created")


def filter_function(
    function_name: str, images: List[DockerImage]
) -> Iterable[DockerImage]:
    """Returns an iterable of images matching a function name"""
    matching_images = filter(lambda x: function_name in x.repository, images)

    if first_image := next(matching_images, 0):
        yield first_image
        for image in matching_images:
            yield image
    else:
        raise ValueError(f"No images matching '{function_name}'")


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
    config = load_config(os.path.join(full_path, config_name))

    # TODO: Check if an existing -t exists and ask if overwrite
    
    # docker build -t new-function ./new_function/
    run_cmd(
        [
            "docker",
            "build",
            "-t",
            f"functions-{config.run_variables.name}",
            f"{full_path}",
        ]
    )


@app.command()
def start(
    function_path: str = typer.Option(
        None,
        help="Name of the function you are running.",
        autocompletion=complete_function_dir,
    ),
):
    # Find the function directory
    # Extract the function name unless specified
    # docker run -ip 8080:8080 --rm --name new-function new-function
    ...


@app.command()
def stop(
    function_name: str = typer.Option(
        None,
        help="Stop a running function",
        autocompletion=complete_function_dir,
    ),
):
    # docker stop name
    # Respond not found if no matching function
    ...


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
    try:
        # Load all functions
        images = get_functions()

        # Print the functions matching the name
        for image in filter_function(function_name, images):
            typer.echo(f"Here are the matching images:")
            typer.echo(image)
    except (ValidationError, ValueError) as error:
        typer.echo(error)
        typer.Exit(code=1)
