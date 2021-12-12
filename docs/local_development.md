# How the get started with running `functions-cli` locally

If you want to run code locally for development, contributions or simply want to adjust a few lines of code here are a few instructions on how to get setup.

## Requirements

This project is developed in python, using `poetry` for dependencies and package management hence you need to have:

- [poetry](https://github.com/python-poetry/poetry)

Installed and available.

Checkout [general package requirements](../README.md#requirements) before moving onward.

## Running from source code

To operate the package from the source code.

1. Download the repository.

    ```bash
    git clone https://github.com/Katolus/functions.git
    ```

2. Ensure that `python` and [`pip`](https://pip.pypa.io/en/stable/installation/) are installed.

3. Using `poetry`, install all package's dependencies by running

    ```bash
    poetry install
    ```

    inside the project's directory.

4. Run `poetry shell` to enter the scope of the package.
5. Run `functions --version` to validate that the package is available correctly. You should see something like this.

   ```console
   You are using 0.1.0a3 version of the functions-cli package
   ```

6. Execute or invoke the commands like you would normally, by running `functions [OPTIONS] COMMAND [ARGS] ...` in the invoked shell.

    **Additionally** you can install the package from source code by building a wheel and installing it manually in your environment's scope.

## Installing from source code

If you want to install package from the repository as a local package (available outside of the `poetry shell` scope), then you might want to build and install following these steps:

1. Run `poetry build` and you should see a `dist` folder appear in the root directory of the code (assuming you are running the command from there).
2. Install the package directly by the while specifying a path to the source - `pip install /home/{your_user}/{project_root_path}/dist/functions_cli-0.1.0a2-py3-none-any.whl`.

Handy tutorial in the scope of the `typer` package, that could help with this -> [here](https://typer.tiangolo.com/tutorial/package/).

Alternatively there run the [`install_locally.sh`](/scripts/install_locally.sh) script.

## Preparing for a new version release

TBU
