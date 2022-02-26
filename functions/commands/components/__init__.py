from functions.core import FTyper

from .docker import app as docker_app
from .gcp import app as gcp_app

app = FTyper(help="Manage the components of the functions package.")

app.add_typer(docker_app, name="docker")
app.add_typer(gcp_app, name="gcp")
