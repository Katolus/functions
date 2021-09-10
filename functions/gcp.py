from typing import List

from functions.processes import run_cmd

# TODO: Add check to make sure that the library installed and if not throw an error

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


class GCPService:
    FUNCTION: str = "cloud_function"
    RUN: str = "cloud_run"

    @classmethod
    def all(cls) -> List[str]:
        return [cls.FUNCTION, cls.RUN]


# TODO: Ensure that the gcloud library is installed first
def current_project() -> str:
    """Returns current working project"""
    output = run_cmd(["gcloud", "config", "get-value", "project"])
    return output.stdout.strip()


def deploy_c_function(function_name: str):
    """Uses gcloud to deploy a cloud function"""
    run_cmd(
        [
            "gcloud",
            "functions",
            "deploy",
            "--set-env-vars",
            # TODO: Add env variables from the config
        ]
    )


def deploy_c_run(function_name: str):
    """Uses gcloud to deploy a cloud run container"""
    ...
