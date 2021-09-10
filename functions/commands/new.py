import os
import json

import typer

from functions import defaults
from functions.system import add_file
from functions.system import make_dir

app = typer.Typer(help="Factory method for creating new functions")


def add_required(
    function_name: str, function_dir: str, *, main_content: str, signature_type: str
):
    """Add required files into the function directory"""
    # Make a new directory
    make_dir(function_dir)
    # Create a confing setup
    add_file(
        function_dir,
        filename="config.json",
        content=json.dumps(defaults.default_config(function_name, signature_type)),
    )

    # Create a Docker file
    add_file(function_dir, filename="Dockerfile", content=defaults.default_docker_file)

    # Create a docker ignore file
    add_file(
        function_dir,
        filename=".dockerignore",
        content=defaults.default_docker_ignore_file,
    )

    # Create a docker ignore file
    add_file(
        function_dir,
        filename="requirements.txt",
        content=defaults.default_requirements_file,
    )

    # Create a default entry point
    add_file(function_dir, filename="main.py", content=main_content)


@app.command()
def pubsub(
    # TODO Add validatation to make sure this is not a path
    function_name: str,
    dir: str = typer.Option(
        ".",
        help="Directory that will be used as a root of the new function",
    ),
):
    """Creates a new pubsub directory"""
    function_dir = os.path.join(dir, function_name)

    add_required(
        function_name,
        function_dir,
        main_content=defaults.default_entry_hello_pubsub,
        signature_type="event",
    )

    typer.echo(f"Added a new pubsub function -> {function_dir}")


@app.command()
def http(
    function_name: str,
    dir: str = typer.Option(
        ".",
        help="Directory that will be used as a root of the new function",
    ),
):
    """Creates a new http directory"""
    function_dir = os.path.join(dir, function_name)

    add_required(
        function_name,
        function_dir,
        main_content=defaults.default_entry_hello_http,
        signature_type="http",
    )

    typer.echo(f"Added a new http function to -> {function_dir}")


if __name__ == "__main__":
    app()
