from functions.config.models import FunctionConfig
from functions.config.models import FunctionRecord
from functions.gcp import errors

from .constants import GCPServices


def deploy(config: FunctionConfig):
    """Deploys the function to GCP"""
    if config.deploy_variables.service == GCPServices.CLOUD_FUNCTION:
        from .cloud_function.cli import deploy_function

        return deploy_function(config)
    else:
        raise errors.UnknownServiceError(config.deploy_variables.service)


def fetch_logs(function: FunctionRecord):
    """Fetches the logs for the function"""
    if function.config.deploy_variables.service == GCPServices.CLOUD_FUNCTION:
        from .cloud_function.cli import fetch_function_logs

        return fetch_function_logs(function)
    else:
        raise errors.UnknownServiceError(function.deploy_variables.service)
