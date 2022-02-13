from functions import logs
from functions import styles
from functions import user
from functions.components import Component
from functions.components.errors import ComponentMissingError
from functions.components.errors import ComponentVersionError
from functions.processes import check_output

# Add a constant that pins a gcloud's version to a minimum one
MAJOR = "367"
MINOR = "0"
PATCH = "0"
MIN_GCP_VERSION = f"{MAJOR}.{MINOR}.{PATCH}"


# Add a function that returns a version of the docker command
def get_gcloud_version() -> str:
    """Returns the version of the docker command"""
    return check_output(["gcloud", "version"]).strip().split("\n")[0].split(" ")[-1]


class GCPComponent(Component):

    NAME = "gcp"
    DESCRIPTION = "GCP's cloud SDK - CLI tool"
    TYPE = "gcp"

    @classmethod
    def is_available(cls) -> bool:
        """
        Returns True if the component is available for the current platform.
        """
        try:
            gcloud_version = get_gcloud_version()
            logs.debug(f"gcloud version: {styles.green(gcloud_version)}")
        except FileNotFoundError as error:
            raise ComponentMissingError(component=cls.TYPE, error=error)

        if gcloud_version.split(".")[0] < MAJOR:
            raise ComponentVersionError(
                component=cls.TYPE, version=gcloud_version, min_version=MIN_GCP_VERSION
            )

        return True

    @classmethod
    def show_instruction(cls) -> None:
        """
        Prints the instructions for installing the component.
        """
        user.inform(
            f"A minium version '{MIN_GCP_VERSION}' of `gcp` is required for interactions with GCP."
        )
        user.inform(
            "Check out the instructions for installing the tool: https://cloud.google.com/sdk/docs/install ."
        )
