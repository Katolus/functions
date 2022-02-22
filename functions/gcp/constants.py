from enum import Enum
from typing import Any, Dict

DEFAULT_GCP_REGION: str = "us-west1"

# Do not use "GOOGLE_*" property names
GCP_RESERVED_VARIABLES: Dict[str, Any] = {
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
        "description": (
            "Reserved: The current identity (service account)" " of the function."
        )
    },
    "FUNCTION_REGION": {
        "description": "Reserved: The function region (example: us-central1)."
    },
    # Newer below
    "FUNCTION_TARGET": {"description": "Reserved: The function to be executed."},
    "FUNCTION_SIGNATURE_TYPE": {
        "description": (
            "Reserved: The type of the function: http for HTTP functions,"
            " and event for event-driven functions."
        )
    },
    "K_SERVICE": {"description": "Reserved: The name of the function resource."},
    "K_REVISION": {"description": "Reserved: The version identifier of the function."},
    "PORT": {"description": "Reserved: The port over which the function is invoked."},
}


class GCPServices(str, Enum):
    """
    Enum of GCP services.
    """

    CLOUD_FUNCTION = "cloud_function"
