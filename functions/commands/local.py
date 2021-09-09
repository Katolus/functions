import os
from typing import Optional

import typer

app = typer.Typer(help="Run functions locally.")

from functions.autocomplete import complete_function_dir
from functions.processes import run_locally
from functions.validation import valid_function_dirs
from functions.config import load_config
from functions.config import get_config_path

@app.command()
def start(
    function_name: str = typer.Option(
        None,
        help="Run a given function locally.",
        autocompletion=complete_function_dir,
    ),
):
    functions = {}
    if function_name:
        typer.echo(f"Running the script for a single function - {function_name}")
        functions[function_name] = get_config_path(function_name)
    else:
        typer.echo(f"Deploying all the available functions.")
        functions = valid_function_dirs()

    # For valid function in functions
    processes = []
    try:
        for function, config_path in functions.items():
            # Get a function directory path
            config = load_config(config_path)
            typer.echo(
                f"Deploying {function} to -> {config.deploy_variables.service}"
            )
            running = run_locally(
                source=os.path.join(function, config.run_variables.source),
                target=config.run_variables.entry_point,
                port=config.run_variables.port,
            )
            processes.append(running)

        exit = typer.confirm("Are you sure you want to delete it?")

    finally:
        for proccess in processes:
            proccess.kill()



if __name__ == "__main__":
    app()
