import typer


def bold(text: str) -> str:
    return typer.style(text, bold=True)


def red(text: str) -> str:
    return typer.style(text, fg=typer.colors.RED)


def yellow(text: str) -> str:
    return typer.style(text, fg=typer.colors.YELLOW)


def blue(text: str) -> str:
    return typer.style(text, fg=typer.colors.BLUE)


def green(text: str) -> str:
    return typer.style(text, fg=typer.colors.GREEN)
