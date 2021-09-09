import typer


from functions.commands import docker
from functions.commands import new
from functions.commands import run


app = typer.Typer(
    help="Run script to executing, testing and deploying included functions."
)

app.add_typer(docker.app, name="docker")
app.add_typer(new.app, name="new")
app.add_typer(run.app, name="run")


@app.command()
def list():
    # TODO Update this command
    from functions.commands.docker import all_functions

    functions = all_functions()
    if functions:
        for function in functions:
            typer.echo(function)
    else:
        typer.echo("No functions found")


if __name__ == "__main__":
    app()
