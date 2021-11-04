"""Holds the information about interaction with remote services"""
from typing import NoReturn

from functions.config.files import FunctionRegistry
from functions.config.models import FunctionConfig
from functions.constants import CloudProvider


def handle_unmatched_provider(provider: str) -> NoReturn:
    """Handles an unmatched provider raise corrent error messages"""
    if provider in CloudProvider.all():
        raise NotImplementedError(f"{provider} is not yet supported")
    else:
        raise Exception("No such provider")


def deploy_function(
    function_name: str, *, config: FunctionConfig, provider: CloudProvider = None
):
    """Deploys a function to a given provider using a defined service"""
    provider = provider or config.deploy_variables.provider

    if provider == CloudProvider.GCP:
        from functions.gcp.services import deploy

        return deploy(function_name, config)
    handle_unmatched_provider(provider)


def read_logs(function_name: str, *, provider: CloudProvider):
    """Reads logs from a given provider using a defined service"""
    function = FunctionRegistry.fetch_function(function_name)

    if provider == CloudProvider.GCP:
        from functions.gcp.services import fetch_logs

        return fetch_logs(function)
    handle_unmatched_provider(provider)
