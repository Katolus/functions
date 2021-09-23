import typer


def bold(text: str) -> str:
    return typer.style(text, bold=True)


def red(text: str) -> str:
    return typer.style(text, fg=typer.colors.RED)


def blue(text: str) -> str:
    return typer.style(text, fg=typer.colors.BLUE)