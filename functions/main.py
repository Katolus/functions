import typer


from functions.commands import build
from functions.commands import new
from functions.commands import run


app = typer.Typer(
    help="Run script to executing, testing and deploying included functions."
)

app.add_typer(build.app, name="build")
app.add_typer(new.app, name="new")
app.add_typer(run.app, name="run")

if __name__ == "__main__":
    app()
