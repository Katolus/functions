from functions import styles
from functions import user
from functions.components.docker import DockerComponent
from functions.core import FTyper

app = FTyper(help="Manage the docker component.")


@app.command()
def check() -> None:
    """
    Check if the docker component is available.
    """
    DockerComponent.is_available()
    user.inform(f"The `docker` component is {styles.green('available')}.")


@app.command()
def instructions() -> None:
    """
    Show instructions for the docker component.
    """
    DockerComponent.show_instruction()
