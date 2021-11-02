"""Holds the information about interaction with remote services"""
from functions.config.models import FunctionConfig
from functions.constants import CloudProvider


def deploy_function(config: FunctionConfig):
    """Deploys a function to a given provider using a defined service"""
    deploy_variables = config.deploy_variables

    if deploy_variables.provider in CloudProvider.supported():
        if config.deploy_variables.provider == CloudProvider.GCP:
            from functions.gcp.cloud_function import manager as gcp_manager

            gcp_manager.deploy(
                config.run_variables.name,
                entry_point=config.run_variables.entry_point,
                runtime=deploy_variables.runtime,
                trigger=deploy_variables.trigger,
            )

    if deploy_variables.provider in CloudProvider.all():
        raise NotImplementedError(f"{deploy_variables.provider} is not yet supported")
    else:
        raise Exception("No such provider")
