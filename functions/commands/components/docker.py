from functions import styles
from functions import user
from functions.components.docker import DockerComponent
from functions.core import FTyper

app = FTyper(help="Manage `docker` component")


@app.command()
def check() -> None:
    """Check the state of the `docker` component"""
    DockerComponent.is_available()
    user.inform(f"The `docker` component is {styles.green('available')}.")


@app.command()
def instructions() -> None:
    """Print instructions for the `docker` component"""
    DockerComponent.show_instruction()
