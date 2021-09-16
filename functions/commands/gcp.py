from pathlib import Path

import typer

from functions.autocomplete import autocomplete_deploy_functions
from functions.gcp import GCPService, deploy_c_function, deploy_c_run
from functions.system import get_config_path, load_config
from functions.types import LocalFunctionDir
from functions.constants import ConfigName


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
    # TODO: Add autocompletion once the build images have their config setup.
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
def delete():
    """Deletes a functions deployed to GCP"""
    raise NotImplementedError()


@app.command()
def logs():
    """Reads log from a deployed function"""
    raise NotImplementedError()
