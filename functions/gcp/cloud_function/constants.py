from enum import Enum

# Example ENV variables
# {
#   "GCF_BLOCK_RUNTIME_go112": "410",
#   "FUNCTION_TARGET": "main",
#   "HOME": "/root",
#   "K_REVISION": "2",
#   "PYTHONUSERBASE": "/layers/google.python.pip/pip",
#   "PYTHONDONTWRITEBYTECODE": "1",
#   "DEBIAN_FRONTEND": "noninteractive",
#   "FUNCTION_SIGNATURE_TYPE": "http",
#   "PORT": "8080",
#   "GCF_BLOCK_RUNTIME_nodejs6": "410",
#   "PWD": "/workspace",
#   "GAE_RUNTIME": "python39",
#   "K_SERVICE": "test-funcion",
#   "PYTHONUNBUFFERED": "1",
#   "PATH": "/layers/google.python.pip/pip/bin:/opt/python3.9/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin", # noqa: E501, W505
#   "S2A_ACCESS_TOKEN": "e13755294ada4a6059f3cf3683a7b2f30b0052938e522063e640386830c6bdab",
#   "LD_LIBRARY_PATH": "/layers/google.python.pip/pip/lib",
#   "LC_CTYPE": "C.UTF-8",
#   "SERVER_SOFTWARE": "gunicorn/20.0.4",
# }


class Runtime(str, Enum):
    """
    Runtime constants for Cloud Functions.
    """

    PYTHON37 = "python37"
    PYTHON38 = "python38"
    PYTHON39 = "python39"
    NODEJS10 = "nodejs10"
    NODEJS12 = "nodejs12"
    NODEJS14 = "nodejs14"
    NODEJS16 = "nodejs16"
    JAVA11 = "java11"
    GO111 = "go111"
    GO113 = "go113"
    GO116 = "go116"
    DOTNET3 = "dotnet3"
    PHP74 = "php74"
    RUBY26 = "ruby26"
    RUBY27 = "ruby27"

    @classmethod
    def validate_supported_versions(cls) -> None:
        """
        Fetches information about the supported versions.
        """
        raise NotImplementedError


class TriggerType(str, Enum):
    """
    Trigger constants for Cloud Functions.
    """

    HTTP = "--trigger-http"
    PUBSUB = "--trigger-topic"
    BUCKET = "--trigger-bucket"


class CloudFunctionLabel(str, Enum):
    """
    Cloud Function label constants.
    """

    MARK = "org-ventress-functions-mark"
    NAME = "org-ventress-functions-name"
    VERSION = "org-ventress-functions-version"


class SignatureType(str, Enum):
    """Cloud function signature types"""

    PUBSUB = "event"
    HTTP = "http"
