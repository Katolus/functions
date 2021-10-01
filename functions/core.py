"""Stores the core logic for the tool's ways of working. 
It is an entry point to the package and all ways lead from here out."""
from typing import Any, Sequence, Tuple

import typer
from pydantic import BaseModel
from pydantic import PrivateAttr

from functions.decorators import handle_error


class FunctionsState(BaseModel):
    """Functions execution state"""

    verbose = False


class Functions(BaseModel):
    """Main class, designed to be a wrapper over an underlying Typer class"""

    _main: typer.Typer = PrivateAttr()
    subcommands: Sequence[Tuple[typer.Typer, str]]
    state: FunctionsState = FunctionsState()

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._main = typer.Typer(
            name="functions-cli",
            help="Run script to executing, testing and deploying included functions.",
        )

        for app, name in self.subcommands:
            self._main.add_typer(app, name=name)

    @handle_error
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self._main.__call__(*args, **kwargs)

    def callback(self, *args, **kwargs):
        return self._main.callback(*args, **kwargs)

    def command(self, *args, **kwargs):
        return self._main.command(*args, **kwargs)

    class Config:
        # typer.Typer
        arbitrary_types_allowed = True