import typer

from functions.autocomplete import autocomplete_deploy_functions
from functions.gcp import GCPService, deploy_c_function, deploy_c_run
from functions.system import get_config_path, load_config
from functions.types import LocalFunctionDir


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
    function_dir: str = typer.Argument(
        ...,
        # It would be great if it supported both image name and path
        help="Name of the function you wish to deploy",
        autocompletion=autocomplete_deploy_functions,
    ),
    service: str = typer.Option(
        GCPService.FUNCTION,
        help="Type of service you want this resource to be deploy to",
        autocompletion=GCPService.all,
    ),
):
    """Deploy a functions to GCP"""
    local_dir: LocalFunctionDir = function_dir
    config_path = get_config_path(local_dir)
    config = load_config(config_path)
    service = service or config.deploy_variables.service
    if service == GCPService.FUNCTION:
        deploy_c_function(config, local_dir)
    elif service == GCPService.RUN:
        deploy_c_run(function_name)
    else:
        # Throw an error
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
