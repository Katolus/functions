from functions import styles
from functions import user
from functions.components.gcp import GCPComponent
from functions.core import FTyper

app = FTyper(help="Manage `GCP` component")


@app.command()
def check() -> None:
    """Check the state of the `GCP` component"""
    GCPComponent.is_available()
    user.inform(f"The `GCP` component is {styles.green('available')}.")


@app.command()
def instructions() -> None:
    """Print instructions for the `GCP` component"""
    GCPComponent.show_instruction()
