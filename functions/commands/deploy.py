"""Deploy a function to cloud"""
from typing import Optional

import typer

from functions.autocomplete import complete_function_dir
from functions.autocomplete import complete_services

app = typer.Typer(help="Deploy your functions")


@app.command()
def deploy(
    function_dir: Optional[str] = typer.Option(
        None,
        help="Run a given function locally.",
        autocompletion=complete_function_dir,
    ),
    service: Optional[str] = typer.Option(
        None,
        help="Pick the services you want to deploy to.",
        autocompletion=complete_services,
    ),
):
    ...

if __name__ == "__main__":
    app()
