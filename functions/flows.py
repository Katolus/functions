"""Store functions that trigger flows of logic that can be reused"""
import os

from functions import actions
from functions import styles
from functions import user
from functions.config.files import FunctionRegistry
from functions.config.models import FunctionConfig
from functions.config.models import FunctionRecord
from functions.constants import FunctionType
from functions.constants import LocalStatus
from functions.system import construct_abs_path


def load_or_generate_config(f_name: str, f_path: str) -> FunctionConfig:
    """Loads a config file from a function directory or generates one if not present"""
    # Check if the config file exists
    if FunctionConfig.check_config_file_exists(f_path):
        # Load the config file
        return FunctionConfig.load(f_path)
    else:
        f_type = actions.ask_for_type_of_function(
            FunctionType.HTTP.value, FunctionType.options()
        )
        # Generate a config instance
        return FunctionConfig.generate(f_name, FunctionType(f_type), f_path)


def abort_if_function_exists(f_name: str) -> None:
    """Abort if a function already exists in the registry"""

    if FunctionRegistry.check_if_function_name_in_registry(f_name):
        user.warn(f"A function with the name {f_name} already exists")
        user.confirm_abort(
            f"Hala, it looks like a function with the name '{f_name}' already exists."
            "Do you want to overwrite?"
        )


def add_function(function_dir: str, ask_config_q: bool = True) -> None:
    """Add a function to the registry"""
    # Get the absolute path
    abs_path = construct_abs_path(function_dir)
    dir_name = os.path.basename(abs_path)

    # Ask the user for a function name if not provided and provide a default
    f_name = actions.ask_for_function_name(dir_name)

    # Ask if abort or overwrite if function exists
    abort_if_function_exists(f_name)

    f_config = load_or_generate_config(f_name, str(abs_path))

    function = FunctionRecord(name=f_name, config=f_config)
    function.set_local_status(LocalStatus.ADDED)
    function.update_registry()

    if ask_config_q and actions.ask_if_config_need_to_be_stored(f_config.path):
        f_config.save()

    user.inform(
        f"{styles.green('Successfully')} added a function to the registry."
        f" The name of the functions is -> {f_name}"
    )
