from functions.processes import check_output

# Add a constant that pins a docker's version to a minimum one
MAJOR = "20"
MINOR = "10"
PATCH = "10"
MIN_DOCKER_VERSION = f"{MAJOR}.{MINOR}.{PATCH}"


# Add a function that returns a version of the docker command
def get_docker_version() -> str:
    """Returns the version of the docker command"""
    return check_output(["docker", "version", "--format", "{{.Server.Version}}"])


# Print an information about the range of versions supported for docker installations
def print_docker_version_range() -> None:
    """Prints the range of docker versions supported"""
    print(f"Minimum docker version: {MIN_DOCKER_VERSION}")
