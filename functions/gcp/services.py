from typing import List

from functions import user
from functions.config.models import FunctionRecord
from functions.constants import CloudServiceType
from functions.gcp import errors
from functions.gcp.cloud_function.constants import CloudFunctionLabel

from .constants import GCPServices


def deploy(function: FunctionRecord) -> None:
    """Deploys the function to GCP"""
    service = function.config.deploy_variables.service

    if service == GCPServices.CLOUD_FUNCTION:
        from .cloud_function.cli import deploy_function

        return deploy_function(function)
    else:
        raise errors.UnknownServiceError(service=service)


def describe(function: FunctionRecord) -> None:
    """Use the `describe` command to retrieve information about a function"""
    service = function.config.deploy_variables.service
    if service == GCPServices.CLOUD_FUNCTION:
        from .cloud_function.cli import run_describe_cmd

        return run_describe_cmd(function)
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


def list_functions(service: CloudServiceType) -> None:
    """Lists all the functions deployed to a given provider using a given service"""
    if service == GCPServices.CLOUD_FUNCTION:
        from .cloud_function.cli import fetch_functions_in_json

        functions = fetch_functions_in_json()

        user.inform(f"Number of functions deployed: {len(functions)}")

        # Iterate over the functions and print the basic information about each
        for function in functions:
            # Update this once there are proper models for cloud functions
            name = function["labels"][CloudFunctionLabel.NAME]
            user.inform(
                f"Function ({name}) is deployed in a {function['runtime']} and was last update at {function['updateTime']}"
            )
    else:
        raise errors.UnknownServiceError(service=service)
