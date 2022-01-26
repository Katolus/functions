"""Stores functions that interact with a user to perform an action"""

from typing import List

from functions import user
from functions.constants import ConfigName


def ask_for_function_name(default: str) -> str:
    """Asks the user for a function name"""
    return user.ask(
        "What should be the name of the function?",
        default=default,
    )


def ask_for_type_of_function(default: str, options: List[str]) -> str:
    """Asks the user for a function type"""
    return user.ask(
        "What type of function is this?",
        default=default,
        options=options,
    )


def ask_if_config_need_to_be_stored(path: str, default: bool = True) -> bool:
    """Asks the user if he wants to store the config in a function directory"""
    return user.confirm(
        f"Do you want to store the config file ({ConfigName.BASE}) in the function's directory ({path})?",
        default=default,
    )
