"""Stores methods for autocompleting GCP commands"""

from typing import Iterable

from functions.config.files import FunctionRegistry
from functions.gcp.services import fetch_deployed_function_names


def gcp_deploy_autocomplete(incomplete: str) -> Iterable[str]:
    """Returns a list of deployable functions"""
    for name in FunctionRegistry.fetch_function_names():
        if name.startswith(incomplete):
            yield name


def gcp_delete_autocomplete(incomplete: str) -> Iterable[str]:
    """Returns a list of resources available for deletion"""
    for name in fetch_deployed_function_names():
        if name.startswith(incomplete):
            yield name


def autocomplete_deployed_function(incomplete: str) -> Iterable[str]:
    """Returns a list of resources available for deletion"""
    for name in fetch_deployed_function_names():
        if name.startswith(incomplete):
            yield name
