"""Stores the core logic for the tool's ways of working.
It is an entry point to the package and all ways lead from here out."""
import functools
from typing import Any, List, Optional, Sequence

import typer
from pydantic import BaseModel
from typer.main import get_command

from functions.components import ComponentEnum
from functions.components import ComponentType
from functions.config.files import AppConfig
from functions.config.managers import AppConfigManager
from functions.decorators import handle_error
from functions.types import AnyCallableT


class FunctionsState(BaseModel):
    """Functions execution state"""

    verbose = False
    components: List[ComponentType] = []


class FTyper(typer.Typer):
    """Wrapper classes an underlying Typer class"""

    is_active: bool = True
    component_type: Optional[ComponentType] = None

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        command = handle_error(get_command(self))
        return command(*args, **kwargs)

    def callback(self, *args: Any, **kwargs: Any) -> AnyCallableT:
        """Wraps the callback decorator to provide a few enhancements"""
        decorator: AnyCallableT = super().callback(*args, **kwargs)

        @functools.wraps(decorator)
        def wrapper(function: AnyCallableT) -> AnyCallableT:
            new_function = handle_error(function)
            return decorator(new_function)

        return wrapper

    def command(
        self,
        *args: Any,
        disable: bool = False,
        **kwargs: Any,
    ) -> AnyCallableT:
        """Wraps the command decorator to provide a few enhancements"""
        # If the component type is not available or the disable flag is set,
        if not self.is_active or disable:
            # Then we can skip the command by not return a callable that does not add it to Typer
            def do_nothing(*args: Any, **kwargs: Any) -> None:
                return None

            return do_nothing

        # Grab the command decorator and wrap it with our own while handling errors
        decorator: AnyCallableT = super().command(*args, **kwargs)

        @functools.wraps(decorator)
        def wrapper(f: AnyCallableT) -> AnyCallableT:
            new_f = handle_error(f)
            return decorator(new_f)

        return wrapper


class NestedCommand(BaseModel):
    """Nested command"""

    command_typer: FTyper
    name: str
    component_type: Optional[ComponentType] = None

    class Config:
        # typer.Typer
        arbitrary_types_allowed = True


def get_nested_commands() -> List[NestedCommand]:
    """Get nested commands"""
    # TODO: Validate if there is a better way to do this
    from functions import commands

    return [
        NestedCommand(command_typer=commands.new, name="new"),
        NestedCommand(
            command_typer=commands.gcp, name="gcp", component_type=ComponentEnum.GCP
        ),
        NestedCommand(command_typer=commands.sync, name="sync"),
        NestedCommand(command_typer=commands.components, name="components"),
    ]


# Add a singleton instance for this class
class FunctionsCli(FTyper):
    """FunctionsCli class, designed prepare the CLI for the functions package"""

    config_manager: AppConfigManager = AppConfigManager()
    state: FunctionsState = FunctionsState()

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(
            name="functions",
            help="CLI tool that helps you manage your (FaaS) components.",
            **kwargs,
        )
        self.is_active = True

        # Set components on state
        self.set_components(self.config.components)

        # Set nested commands on main
        self.set_nested_commands()

    @property
    def config(self) -> AppConfig:
        """Shortcut to the app's config instance"""
        return self.config_manager.app_config.load()

    def set_components(self, components: Sequence[ComponentType]) -> None:
        """Sets the components to the state"""
        for component in components:
            self.state.components.append(component)

    def set_nested_commands(self):
        """Sets the nested commands"""
        for command in get_nested_commands():
            if (
                command.component_type is not None
                and command.component_type not in self.state.components
            ):
                # If the component type is not available, we can skip the command by not adding it
                continue
            self.add_typer(command.command_typer, name=command.name)

    class Config:
        # typer.Typer
        arbitrary_types_allowed = True
