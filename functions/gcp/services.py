from typing import List

from functions.config.models import FunctionRecord
from functions.gcp import errors

from .constants import GCPServices


def deploy(function: FunctionRecord) -> None:
    """Deploys the function to GCP"""
    service = function.config.deploy_variables.service

    if service == GCPServices.CLOUD_FUNCTION:
        from .cloud_function.cli import deploy_function

        return deploy_function(function)
    else:
        raise errors.UnknownServiceError(service=service)


def fetch_logs(function: FunctionRecord) -> None:
    """Fetches the logs for the function"""
    service = function.config.deploy_variables.service
    if service == GCPServices.CLOUD_FUNCTION:
        from .cloud_function.cli import fetch_function_logs

        return fetch_function_logs(function)
    else:
        raise errors.UnknownServiceError(service=service)


def fetch_deployed_function_names() -> List[str]:
    """Fetches the deployed function names"""
    from .cloud_function.cli import fetch_deployed_function_names

    return fetch_deployed_function_names()
