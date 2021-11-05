"""Holds functions that ask a user for input"""
import warnings
from typing import List

import typer

from functions import logs
from functions import styles
from functions.config.models import FunctionConfig


def ask(question: str, default: str = None, options: List[str] = None) -> str:
    if options:
        question += f"{styles.yellow(' Options')}[{', '.join(options)}]"

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


def prompt_to_save_config(config: FunctionConfig) -> None:
    """Asks the user if he wants to save the config in a function directory"""
    store_config_file = confirm(
        f"Do you want to store the configuration file in the function's directory ({config.path})?",
        default=True,
    )

    if store_config_file:
        config.save()
