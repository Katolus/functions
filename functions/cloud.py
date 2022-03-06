"""Holds the information about interaction with remote services"""
from typing import NoReturn

from functions.config.files import FunctionRegistry
from functions.config.models import FunctionRecord
from functions.constants import CloudProvider
from functions.constants import CloudServiceType


def handle_unmatched_provider(provider: str) -> NoReturn:
    """Handles an unmatched provider raise corrent error messages"""
    if provider in CloudProvider.all():
        raise NotImplementedError(f"{provider} is not yet supported")
    else:
        raise Exception("No such provider")


def deploy_function(function: FunctionRecord, /, provider: CloudProvider = None):
    """Deploys a function to a given provider using a defined service"""
    provider = provider or function.config.deploy_variables.provider

    if provider == CloudProvider.GCP:
        from functions.gcp.services import deploy

        return deploy(function)
    handle_unmatched_provider(provider)


def describe_function(
    function: FunctionRecord, /, provider: CloudProvider = None
) -> None:
    """Describes a function on a given provider using a defined service"""
    provider = provider or function.config.deploy_variables.provider

    if provider == CloudProvider.GCP:
        from functions.gcp.services import describe

        return describe(function)
    handle_unmatched_provider(provider)


def list_functions(
    *, provider: CloudProvider, service: CloudServiceType = None
) -> None:
    """Lists all the functions deployed to a given provider using a defined service"""
    if provider == CloudProvider.GCP:
        from functions.gcp.services import list_functions

        return list_functions(service=service)
    handle_unmatched_provider(provider)


def read_logs(function_name: str, *, provider: CloudProvider):
    """Reads logs from a given provider using a defined service"""
    function = FunctionRegistry.fetch_function(function_name)

    if provider == CloudProvider.GCP:
        from functions.gcp.services import fetch_logs

        return fetch_logs(function)
    handle_unmatched_provider(provider)
