from functions.config.models import FunctionConfig
from functions.gcp import errors

from .constants import GCPServices


def deploy(config: FunctionConfig):
    """Deploys the function to GCP"""
    if config.deploy_variables.service == GCPServices.CLOUD_FUNCTIONS:
        from .cloud_function.cli import deploy_function

        return deploy_function(config)
    else:
        raise errors.UnknownServiceError(config.deploy_variables.service)
