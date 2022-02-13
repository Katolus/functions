from functions import logs
from functions import styles
from functions import user
from functions.components import Component
from functions.components.errors import ComponentMissingError
from functions.components.errors import ComponentVersionError
from functions.processes import check_output

# Add a constant that pins a docker's version to a minimum one
MAJOR = "20"
MINOR = "10"
PATCH = "10"
MIN_DOCKER_VERSION = f"{MAJOR}.{MINOR}.{PATCH}"


# Add a function that returns a version of the docker command
def get_docker_version() -> str:
    """Returns the version of the docker command"""
    return check_output(
        ["docker", "version", "--format", "{{.Server.Version}}"]
    ).strip()


class DockerComponent(Component):

    NAME = "docker"
    DESCRIPTION = "Docker engine"
    TYPE = "docker"

    @classmethod
    def is_available(cls) -> bool:
        """
        Returns True if the component is available for the current platform.
        """
        try:
            docker_version = get_docker_version()
            logs.debug(f"Docker version: {styles.green(docker_version)}")
        except FileNotFoundError as error:
            raise ComponentMissingError(component=cls.TYPE, error=error)

        if docker_version.split(".")[0] < MAJOR:
            raise ComponentVersionError(component=cls.TYPE, version=docker_version)

        return True

    @classmethod
    def show_instruction(cls) -> None:
        """
        Prints the instructions for installing the component.
        """
        user.inform(
            f"A minium version '{MIN_DOCKER_VERSION}' of `docker` is required to run the functions locally."
        )
        user.inform(
            "Check out the instructions for installing docker: https://docs.docker.com/engine/install/ ."
        )
