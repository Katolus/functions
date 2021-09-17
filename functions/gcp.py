import itertools
from typing import List, Optional

from pydantic import validate_arguments

from functions.constants import CloudServiceType
from functions.processes import run_cmd
from functions.types import FunctionConfig, LocalFunctionPath, NotEmptyStr

# TODO: Add check to make sure that the library installed and if not throw an error

GCP_REGION = "australia-southeast1"

GCP_ENV_VARIABLES = {
    "ENTRY_POINT": {"description": "Reserved: The function to be executed."},
    "GCP_PROJECT": {"description": "Reserved: The current GCP project ID."},
    "GCLOUD_PROJECT": {
        "description": "Reserved: The current GCP project ID (deprecated)."
    },
    "GOOGLE_CLOUD_PROJECT": {
        "description": "Reserved: Not set but reserved for internal use."
    },
    "FUNCTION_TRIGGER_TYPE": {
        "description": "Reserved: The trigger type of the function."
    },
    "FUNCTION_NAME": {"description": "Reserved: The name of the function resource."},
    "FUNCTION_MEMORY_MB": {
        "description": "Reserved: The maximum memory of the function."
    },
    "FUNCTION_TIMEOUT_SEC": {
        "description": "Reserved: The execution timeout in seconds."
    },
    "FUNCTION_IDENTITY": {
        "description": "Reserved: The current identity (service account) of the function."
    },
    "FUNCTION_REGION": {
        "description": "Reserved: The function region (example: us-central1)."
    },
    # Newer below
    "FUNCTION_TARGET": {"description": "Reserved: The function to be executed."},
    "FUNCTION_SIGNATURE_TYPE": {
        "description": "Reserved: The type of the function: http for HTTP functions, and event for event-driven functions."
    },
    "K_SERVICE": {"description": "Reserved: The name of the function resource."},
    "K_REVISION": {"description": "Reserved: The version identifier of the function."},
    "PORT": {"description": "Reserved: The port over which the function is invoked."},
}


class GCPCloudFunction:
    @classmethod
    def add_trigger_arguments(cls) -> List[str]:
        """Returns a list of arguments to append that denote the type of trigger applied"""
        # TODO: To Implement
        return ["--trigger-http"]

    @classmethod
    def add_runtime_arguments(cls) -> List[str]:
        """Returns runtime arguments"""
        # TODO: To Implement
        return ["--runtime", "python39"]

    @classmethod
    def add_source_arguments(cls, function_dir: str) -> List[str]:
        """Returns source arguments"""
        # TODO: To Implement
        return ["--source", str(function_dir)]


def add_env_vars_arguments() -> List[str]:
    """Adds environmental variables to the scope of the deployment if any are present"""
    # TODO: To Implement
    return []


@validate_arguments
def add_entry_point_arguments(entry_point: NotEmptyStr) -> List[str]:
    # TODO: Validate that the entry point has more than just empty string
    """Adds entry point variables to the scope of the deployment"""
    # https://cloud.google.com/sdk/gcloud/reference/functions/deploy#--set-env-vars
    return ["--entry-point", entry_point]


def add_ignore_file_arguments(files: Optional[List[str]] = None) -> List[str]:
    """Adds ignore file variables to the scope of the deployment"""
    # TODO: To Implement
    default_ignores = ["config.json", "Dockerfile", ".dockerignore"]
    if not files:
        ingore_files = default_ignores
    else:
        ingore_files = files + default_ignores

    return list(
        itertools.chain.from_iterable(
            [["--ignore-file", filename] for filename in ingore_files]
        )
    )


def add_region_argument() -> List[str]:
    return ["--region", GCP_REGION]


# TODO: Ensure that the gcloud library is installed first
def current_project() -> str:
    """Returns current working project"""
    output = run_cmd(["gcloud", "config", "get-value", "project"])
    return output.stdout.strip()


def deploy_function(config: FunctionConfig, service_type: ServiceType):
    """Deploys a function to a given service"""
    if service_type == CloudServiceType.CLOUD_FUNCTION:
        deploy_c_function(config)
    else:
        raise NotImplementedError()


def delete_function(function_name: str):
    """Runs a gcloud command to remove a function matching a given name"""
    run_cmd(
        [
            "gcloud",
            "functions",
            "delete",
            function_name,
        ]
        + add_region_argument()
    )


@validate_arguments
def deploy_c_function(config: FunctionConfig, function_dir: LocalFunctionPath = None):
    """Uses gcloud to deploy a cloud function"""
    cloud_function_name = config.run_variables.name
    run_cmd(
        [
            "gcloud",
            "functions",
            "deploy",
            cloud_function_name,
        ]
        + GCPCloudFunction.add_runtime_arguments()
        + GCPCloudFunction.add_source_arguments(str(function_dir or config.path))
        + add_entry_point_arguments(config.run_variables.entry_point)
        + add_ignore_file_arguments()
        + add_region_argument()
        + add_env_vars_arguments()
        + GCPCloudFunction.add_trigger_arguments()
    )


def deploy_c_run(function_name: str):
    """Uses gcloud to deploy a cloud run container"""
    raise NotImplementedError("gcloud run is not implemented yet")
