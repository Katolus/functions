import typer

from functions.autocomplete import autocomplete_function_names
from functions.autocomplete import autocomplete_running_function_names
from functions.autocomplete import complete_function_dir
from functions.commands import new
from functions.docker import all_functions
from functions.docker import docker_client
from functions.docker import DockerLabel
from functions.docker import get_config_from_image
from functions.system import construct_config_path
from functions.system import get_full_path
from functions.system import load_config
from functions.validation import validate_dir


app = typer.Typer(
    help="Run script to executing, testing and deploying included functions."
)

app.add_typer(new.app, name="new")


@app.command()
def build(
    function_path: str = typer.Argument(
        ...,
        help="Path to the functions you want to build",
    ),
    config_name: str = typer.Option("config.json", help="Name of a config file"),
):
    # Get the absolute path
    full_path = get_full_path(function_path)

    # Validate that it is a valid path (throw an error if not)
    validate_dir(full_path)

    # Load configuration
    config_path = construct_config_path(full_path, config_name)
    config = load_config(config_path)

    # TODO: Check if an existing -t exists and ask if overwrite

    # Formulate a function tag
    function_name = config.run_variables.name

    image, logs = docker_client.images.build(
        path=str(full_path),
        tag=function_name,
        # buildargs={"CONFIG_PATH": config_path, "FUNC_TAG": function_name},
        # TODO: Store a configuration path as a label
        labels={
            DockerLabel.CONFIG: str(config_path),
            DockerLabel.ORGANISATION: "Ventress",
            DockerLabel.TAG: function_name,
        },
    )

    # TODO: Add color
    typer.echo(f"Successfully build a function's image of {function_name}")


@app.command()
def start(
    function_name: str = typer.Argument(
        ...,
        help="Name of the function you are running.",
        autocompletion=autocomplete_function_names,
    ),
):
    """Start a container for a given function"""
    docker_image = docker_client.images.get(function_name)
    config = get_config_from_image(docker_image)

    container = docker_client.containers.run(
        docker_image,
        ports={config.run_variables.port: "8080"},
        remove=True,
        name=function_name,
        detach=True,
    )


@app.command()
def stop(
    function_name: str = typer.Argument(
        ...,
        help="Name of the functions to stop",
        autocompletion=autocomplete_running_function_names,
    ),
):
    # TODO: Add an option to stop them all
    # TODO: Add a catch for when the name does not match
    container = docker_client.containers.get(function_name)
    container.stop()


@app.command()
def status(
    function_name: str = typer.Option(
        None,
        help="Give status of a function",
        autocompletion=complete_function_dir,
    ),
):

    ...


@app.command()
def list():
    """List existing functions"""
    functions = all_functions()
    if functions:
        for function in functions:
            typer.echo(function)
    else:
        typer.echo("No functions found")


@app.command()
def remove():
    # TODO: Implement
    ...


@app.command()
def rebuild():
    # TODO: Implement
    ...


if __name__ == "__main__":
    app()
