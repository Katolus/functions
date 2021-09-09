import typer

app = typer.Typer(help="Build a function")

from functions.autocomplete import complete_function_dir

@app.command()
def build(
    function_dir: str = typer.Option(
        None,
        help="Build an image of a function.",
        autocompletion=complete_function_dir,
    )
):
    # Build the image given a docker file (TODO: look into - `buildctl` )
    # Scan for vulnerabilities unless flag is specified (store output or notify)
    # Push the built image into a repository
    print('Build')


if __name__ == "__main__":
    app()