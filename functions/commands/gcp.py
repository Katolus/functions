import typer

from functions.gcp import GCPService, deploy_c_function, deploy_c_run


app = typer.Typer(help="Deploy functions in GCP")


@app.command()
def install():
    """Install required libraries"""
    pass


@app.command()
def update():
    """Update required libraries"""
    pass


@app.command()
def deploy(
    function_name: str = typer.Argument(
        ...,
        # It would be great if it supported both image name and path
        help="Name of the function you wish to deploy",
    ),
    service: str = typer.Option(
        GCPService.FUNCTION,
        help="Type of service you want this resource to be deploy to",
        autocompletion=GCPService.all,
    ),
):
    """Deploy a functions to GCP"""
    # Check if function is a path ? look for the directory and deploy that one
    # If the functions is an image try to deploy a
    if service == GCPService.FUNCTION:
        deploy_c_function(function_name)
    elif service == GCPService.RUN:
        deploy_c_run(function_name)
    else:
        # Throw an error
        ...
    ...
