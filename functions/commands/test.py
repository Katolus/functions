from typing import Optional

import typer

from functions.autocomplete import autocomplete_function_names

app = typer.Typer(help="Run tests")


@app.command()
def test(
    function_name: Optional[str] = typer.Option(
        None,
        help="Run tests for a given function or for all if not specified",
        autocompletion=autocomplete_function_names,
    )
):
    raise NotImplementedError()

if __name__ == "__main__":
    app()
