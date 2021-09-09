from typing import Optional

import typer

from functions.autocomplete import complete_function_dir

app = typer.Typer(help="Run tests")


@app.command()
def test(
    function_name: Optional[str] = typer.Option(
        None,
        help="Run tests for a given function or for all if not specified",
        autocompletion=complete_function_dir,
    )
):
    if function_name:
        typer.echo(f"Bye {function_name}")
    else:
        typer.echo("Goodbye!")


if __name__ == "__main__":
    app()
