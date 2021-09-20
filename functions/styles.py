import typer


def bold(text: str) -> str:
    return typer.style(text, bold=True)
