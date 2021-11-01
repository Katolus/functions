import os
from pathlib import Path

import typer

from functions import defaults
from functions import user
from functions.arguments import FunctionNameArgument
from functions.callbacks import function_dir_callback
from functions.config import store_function_info_to_registry
from functions.constants import FunctionStatus
from functions.constants import SignatureType
from functions.system import add_required_files

app = typer.Typer(help="Factory method for creating new functions")


@app.command()
def pubsub(
    function_name: str = FunctionNameArgument(...),
    function_dir: str = typer.Option(
        None,
        "--dir",
        callback=function_dir_callback,
        help="Directory that will be used as a root of the new function",
    ),
) -> None:
    """Creates a new pubsub directory"""
    function_path = os.path.join(function_dir, function_name)

    config = add_required_files(
        function_name,
        function_path,
        main_content=defaults.default_entry_hello_pubsub,
        signature_type=SignatureType.PUBSUB,
    )

    # Add function to functions' function registry
    store_function_info_to_registry(function_name, config, FunctionStatus.NEW)

    user.inform(f"Added a new pubsub function -> {function_path}")


@app.command()
def http(
    function_name: str = FunctionNameArgument(...),
    function_dir: Path = typer.Option(
        None,
        "--dir",
        callback=function_dir_callback,
        help="Directory that will be used as a root of the new function",
    ),
) -> None:
    """Creates a new http directory"""
    function_path = os.path.join(function_dir, function_name)

    config = add_required_files(
        function_name,
        function_path,
        main_content=defaults.default_entry_hello_http,
        signature_type=SignatureType.HTTP,
    )

    store_function_info_to_registry(function_name, config, FunctionStatus.NEW)

    user.inform(f"Added a new http function to -> {function_path}")
