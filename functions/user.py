"""Holds functions that ask a user for input"""
import warnings
from typing import List

import typer

from functions import logs
from functions import styles


def ask(question: str, default: str = None, options: List[str] = None) -> str:
    if options:
        question += f" ({', '.join(options)})"

    return typer.prompt(
        question,
        default=default,
    )


def confirm(question: str, default: bool = False) -> bool:
    return typer.confirm(question, default=default)


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
        warnings.warn(f"{styles.yellow('WARNING: ')}{msg}")


def fail(msg: str, log=True) -> None:
    """Inform a user about a failed execution"""
    if log:
        logs.error(logs.remove_empty_lines_from_string(msg))
    else:
        warnings.warn(msg)
