"""Holds functions that ask a user for input"""
import typer

from functions import logs


def ask(question: str) -> str:
    return typer.prompt(question)


def confirm(question: str) -> bool:
    return typer.confirm(question)


def confirm_abort(question: str) -> bool:
    return typer.confirm(question, abort=True)


def inform(msg: str, log=True) -> None:
    """Informs a user about something."""
    if log:
        logs.info(msg)
    else:
        typer.echo(msg)


def warn(msg: str, log=True) -> None:
    """Warn a user about something."""
    if log:
        logs.warn(msg)
    else:
        typer.echo(msg)