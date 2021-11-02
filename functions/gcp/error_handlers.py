import typer

from functions import logs
from functions import user
from functions.error_handlers import error_handler
from functions.types import ExceptionClass

from .errors import UnknownServiceError


@error_handler(error=UnknownServiceError)
def handle_unknown_gcp_service(error: ExceptionClass):
    """
    Handles an unknown GCP service error.
    """
    logs.error(str(error))
    # Insert function name and service name into error message
    user.warn(
        " ".join(
            [
                "Current functions has missconfigured service.",
                "Such service is not supported.",
                "Please check your configuration.",
            ]
        )
    )
    typer.Exit()
