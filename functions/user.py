"""Holds functions that ask a user for input"""
import warnings

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
        logs.info(logs.remove_empty_lines_from_string(msg))
    else:
        typer.echo(msg)


def warn(msg: str, log=True) -> None:
    """Warning to a user about something."""
    if log:
        logs.warning(logs.remove_empty_lines_from_string(msg))
    else:
        warnings.warn(msg)
