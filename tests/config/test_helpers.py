import os
import sys

import pytest  # type: ignore

from functions.constants import PACKAGE_CONFIG_DIR_PATH


# Skip if sys.platform is not linux
@pytest.mark.skipif(not sys.platform.startswith("linux"), reason="Linux only")
def test_getting_default_system_config_path_for_linux():
    # Set home environment variable to home/user
    os.environ["HOME"] = "/home/user"
    assert PACKAGE_CONFIG_DIR_PATH == "/home/user/.config"


# Skip if sys.platform is not windows
@pytest.mark.skipif(not sys.platform.startswith("win32"), reason="Windows only")
def test_getting_default_system_config_path_for_windows():
    # Set APPDATA environment variable
    os.environ["APPDATA"] = "C:\\Users\\user\\AppData\\"
    assert PACKAGE_CONFIG_DIR_PATH == "C:\\Users\\user\\AppData\\config"


# Skip if sys.platform is not darwin
@pytest.mark.skipif(not sys.platform.startswith("darwin"), reason="Darwin only")
def test_getting_default_system_config_path_for_darwin():
    # Set Darwin HOME environment variable
    os.environ["HOME"] = "/Users/user"
    assert PACKAGE_CONFIG_DIR_PATH == "Unknown"
