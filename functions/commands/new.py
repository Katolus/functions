import os
from pathlib import Path

import typer

from functions import defaults
from functions.arguments import FunctionNameArgument
from functions.callbacks import function_dir_callback
from functions.system import add_required_files

app = typer.Typer(help="Factory method for creating new functions")


@app.command()
def pubsub(
    function_name: str = FunctionNameArgument(...),
    dir: str = typer.Option(
        None,
        callback=function_dir_callback,
        help="Directory that will be used as a root of the new function",
    ),
):
    """Creates a new pubsub directory"""
    function_dir = os.path.join(dir, function_name)

    add_required_files(
        function_name,
        function_dir,
        main_content=defaults.default_entry_hello_pubsub,
        signature_type="event",
    )

    typer.echo(f"Added a new pubsub function -> {function_dir}")


@app.command()
def http(
    function_name: str = FunctionNameArgument(...),
    dir: Path = typer.Option(
        None,
        callback=function_dir_callback,
        help="Directory that will be used as a root of the new function",
    ),
):
    """Creates a new http directory"""
    function_dir = os.path.join(dir, function_name)

    add_required_files(
        function_name,
        function_dir,
        main_content=defaults.default_entry_hello_http,
        signature_type="http",
    )

    typer.echo(f"Added a new http function to -> {function_dir}")
