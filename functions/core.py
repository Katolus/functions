"""Stores the core logic for the tool's ways of working.
It is an entry point to the package and all ways lead from here out."""
import functools
from typing import Any, Sequence, Tuple

import typer
from pydantic import BaseModel
from pydantic import PrivateAttr
from typer.main import get_command

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

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        command = handle_error(get_command(self._main))
        return command(*args, **kwargs)

    def callback(self, *args, **kwargs):
        decorator = self._main.callback(*args, **kwargs)

        @functools.wraps(decorator)
        def wrapper(f):
            new_f = handle_error(f)
            return decorator(new_f)

        return wrapper

    def command(self, *args, **kwargs):
        decorator = self._main.command(*args, **kwargs)

        @functools.wraps(decorator)
        def wrapper(f):
            new_f = handle_error(f)
            return decorator(new_f)

        return wrapper

    class Config:
        # typer.Typer
        arbitrary_types_allowed = True
