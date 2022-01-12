"""Stores the core logic for the tool's ways of working.
It is an entry point to the package and all ways lead from here out."""
import functools
from typing import Any, List, Optional, Sequence

import typer
from pydantic import BaseModel
from pydantic import PrivateAttr
from typer.main import get_command

from functions import commands
from functions.components import ComponentEnum
from functions.components import ComponentType
from functions.config.files import AppConfig
from functions.config.managers import AppConfigManager
from functions.decorators import handle_error


class FunctionsState(BaseModel):
    """Functions execution state"""

    verbose = False
    components: List[ComponentType] = []

    def set_components(self, components: Sequence[ComponentType]) -> None:
        """Sets the components to the state"""
        self.components = components


class NestedCommand(BaseModel):
    """Nested command"""

    command_typer: typer.Typer
    component_type: Optional[ComponentType] = None
    name: str

    class Config:
        # typer.Typer
        arbitrary_types_allowed = True


# Add a singleton instance for this class
class FunctionsCli(BaseModel):
    """FunctionsCli class, designed to be a wrapper over an underlying Typer class"""

    _main: typer.Typer = PrivateAttr()
    config_manager: AppConfigManager = AppConfigManager()
    state: FunctionsState = FunctionsState()

    def __init__(self, **data: Any) -> None:
        self._main = typer.Typer(
            name="functions",
            help="Run script to executing, testing and deploying included functions.",
        )

        super().__init__(**data)

        # Set components on state
        self.state.set_components(self.config.components)

        # Set nested commands on main
        self.set_nested_commands()

    @property
    def config(self) -> AppConfig:
        """Shortcut to the app's config instance"""
        return self.config_manager.app_config.load()

    def get_nested_commands(self) -> List[NestedCommand]:
        return [
            NestedCommand(command_typer=commands.new, name="new"),
            NestedCommand(
                command_typer=commands.gcp, name="gcp", component_type=ComponentEnum.GCP
            ),
            NestedCommand(command_typer=commands.sync, name="sync"),
            NestedCommand(command_typer=commands.components, name="components"),
        ]

    def set_nested_commands(self):
        """Sets the nested commands"""
        for command in self.get_nested_commands():
            if (
                command.component_type is not None
                and command.component_type not in self.state.components
            ):
                # If the component type is not available, we can skip the command by not adding it
                continue
            self._main.add_typer(command.command_typer, name=command.name)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        command = handle_error(get_command(self._main))
        return command(*args, **kwargs)

    def callback(self, *args: Any, **kwargs: Any):
        """Wraps the callback decorator to provide a few enhancements"""
        decorator = self._main.callback(*args, **kwargs)

        @functools.wraps(decorator)
        def wrapper(f):
            new_f = handle_error(f)
            return decorator(new_f)

        return wrapper

    def command(
        self,
        *args: Any,
        component_type: Optional[ComponentType] = None,
        disable: bool = False,
        **kwargs: Any,
    ):
        """Wraps the command decorator to provide a few enhancements"""
        # If the component type is not available or the disable flag is set,
        if (
            component_type is not None and component_type not in self.state.components
        ) or disable:
            # Then we can skip the command by not return a callable that does not add it to Typer
            def do_nothing(*args: Any, **kwargs: Any) -> None:
                return None

            return do_nothing

        # Grab the command decorator and wrap it with our own while handling errors
        decorator = self._main.command(*args, **kwargs)

        @functools.wraps(decorator)
        def wrapper(f):
            new_f = handle_error(f)
            return decorator(new_f)

        return wrapper

    class Config:
        # typer.Typer
        arbitrary_types_allowed = True
