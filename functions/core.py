"""Stores the core logic for the tool's ways of working. 
It is an entry point to the package and all ways lead from here out."""
from typing import Any

from pydantic import BaseModel


class FunctionsApp(BaseModel):
    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        app = typer.Typer(
            name="functions-cli",
            help="Run script to executing, testing and deploying included functions.",
        )
        state = {"verbose": False}

        # TODO: Add a scope if the package is installed
        # if gcloud_is_installed
        app.add_typer(gcp.app, name="gcp")
        app.add_typer(new.app, name="new")
    # state/
    # typer
    # command wrappers