"""Holds the information about interaction with remote services"""
from functions.config.models import FunctionConfig
from functions.constants import CloudProvider


def deploy_function(config: FunctionConfig, provider: CloudProvider = None):
    """Deploys a function to a given provider using a defined service"""
    deploy_variables = config.deploy_variables
    provider = provider or deploy_variables.provider

    if config.deploy_variables.provider == CloudProvider.GCP:
        from functions.gcp.services import deploy

        return deploy(config)
    if deploy_variables.provider in CloudProvider.all():
        raise NotImplementedError(f"{deploy_variables.provider} is not yet supported")
    else:
        raise Exception("No such provider")
