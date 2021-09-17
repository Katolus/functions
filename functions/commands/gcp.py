from pathlib import Path

import typer

from functions.autocomplete import autocomplete_deploy_functions
from functions.input import confirm_abort
from functions.gcp import GCPService, delete_function, deploy_c_function, deploy_c_run, deploy_function
from functions.system import load_config


app = typer.Typer(help="Deploy functions in GCP")


@app.command()
def install():
    """Install required libraries"""
    raise NotImplementedError()


@app.command()
def update():
    """Update required libraries"""
    raise NotImplementedError()


@app.command()
def deploy(
    function_dir: Path = typer.Argument(
        ...,
        # It would be great if it supported both image name and path
        autocompletion=autocomplete_deploy_functions,
        exists=True,
        file_okay=False,
        help="Path to the functions you want to deploy",
        resolve_path=True,
    ),
    # TODO: Make service an enum
    service: str = typer.Option(
        GCPService.FUNCTION,
        help="Type of service you want this resource to be deploy to",
        autocompletion=GCPService.all,
    ),
):
    """Deploy a functions to GCP"""
    config = load_config(function_dir)
    service = service or config.deploy_variables.service

    if service == GCPService.FUNCTION:
        deploy_c_function(config, function_dir)
        pass
    elif service == GCPService.RUN:
        deploy_c_run(config)
    else:
        raise NotImplementedError()
        ...
    ...


@app.command()
def delete(
        function_name: str = typer.Argument(
        ...,
        help="Name of the function you want to remove",
    ),
):
    """Deletes a functions deployed to GCP"""
    # TODO: Implement a delete option with a confirmation
    confirm_abort(f"Are you sure you want to remove '{function_name}'?")
    delete_function(function_name)


@app.command()
def logs():
    """Reads log from a deployed function"""
    raise NotImplementedError()
