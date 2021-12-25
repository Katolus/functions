import typer

from .docker import app as docker_app
from .gcp import app as gcp_app

app = typer.Typer(help="Manage CLI's components")

app.add_typer(docker_app, name="docker")
app.add_typer(gcp_app, name="gcp")
