import typer

from functions import logs
from functions import user
from functions.error_handlers import error_handler
from functions.types import ExceptionClass

from .errors import GCPCommandError


@error_handler(error=GCPCommandError)
def handle_gcp_command_error(error: ExceptionClass):
    """
    Handles an unknown GCP service error.
    """
    logs.error(str(error))
    # Insert function name and service name into error message
    user.inform(f"An error occurred while using the command. Error: {str(error)}")
    typer.Exit()
