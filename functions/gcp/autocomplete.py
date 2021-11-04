"""Stores methods for autocompleting GCP commands"""

from typing import Iterable

from functions.config.files import FunctionRegistry


def gcp_deploy_autocomplete(incomplete: str) -> Iterable[str]:
    """Returns a list of deployable functions"""
    for name in FunctionRegistry.fetch_function_names():
        if name.startswith(incomplete):
            yield name
