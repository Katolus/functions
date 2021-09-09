import typer

from functions.commands import docker

app = typer.Typer(help="Run functions locally")


app.add_typer(docker.app, name="docker")
