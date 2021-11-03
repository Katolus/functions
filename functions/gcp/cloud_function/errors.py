from functions.errors import _DerivedError


class GCPCommandError(_DerivedError):
    """
    Exception raised when deployment fails.
    """

    code = "gcp.command_error"
    msg_template = "Couldn't finish the GCP command. Error: {error}"
