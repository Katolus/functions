"""Holds functions that ask a user for input"""
import warnings
from typing import List

import typer

from functions import logs
from functions import styles
from functions.config.models import FunctionConfig
from functions.constants import ConfigName


def ask(question: str, default: str = None, options: List[str] = None) -> str:
    """A string user prompt of the user in the console"""
    if options:
        question += f"{styles.yellow(' Options')}[{', '.join(options)}]"

    return typer.prompt(
        question,
        default=default,
    )


def confirm(question: str, default: bool = False) -> bool:
    """A boolean confirm prompt of the user in the console"""
    return typer.confirm(question, default=default)


def confirm_abort(question: str) -> bool:
    """A boolean confirm prompt of the user in the console with a default abort action"""
    return typer.confirm(question, abort=True)


def inform(msg: str, log: bool = True) -> None:
    """Informs a user with a message"""
    if log:
        logs.info(logs.remove_empty_lines_from_string(msg))
    else:
        typer.echo(msg)


def warn(msg: str, log: bool = True) -> None:
    """Warning a user with message"""
    if log:
        logs.warning(logs.remove_empty_lines_from_string(msg))
    else:
        warnings.warn(f"{styles.yellow('WARNING: ')}{msg}")


def fail(msg: str, log: bool = True) -> None:
    """Inform a user about a failed execution"""
    if log:
        logs.error(logs.remove_empty_lines_from_string(msg))
    else:
        warnings.warn(msg)


def prompt_to_save_config(config: FunctionConfig) -> None:
    """Asks the user if he wants to save the config in a function directory"""
    store_config_file = confirm(
        f"Do you want to store the configuration file ({ConfigName.BASE}) in the function's directory ({config.path})?",
        default=True,
    )

    if store_config_file:
        config.save()
