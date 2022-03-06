from functions.errors import FunctionBaseError


class GCPCommandError(FunctionBaseError):
    """
    Exception raised when deployment fails.
    """

    code = "gcp.command_error"
    msg_template = "Couldn't finish the GCP command. Error: {error_msg}"
